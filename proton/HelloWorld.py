from __future__ import print_function, unicode_literals
import sys
import threading
from proton import Message
from proton.handlers import MessagingHandler, TransactionHandler
from proton.reactor import ApplicationEvent, Container, EventInjector

class HelloWorld(MessagingHandler):
    def __init__(self, server, address):
        super(HelloWorld, self).__init__()
        self.server = server
        self.address = address

    def on_start(self, event):
        self.container = event.container
        conn = event.container.connect(self.server, allowed_mechs=str("CRAM-MD5"))
        event.container.create_receiver(conn, self.address)
        self.sender = event.container.create_sender(conn, self.address)

    def on_sendable(self, event):
        #event.sender.send(Message(body="Hello World!"))
        #event.sender.close()
        pass

    def on_message(self, event):
        print(event.message.body)
        #event.connection.close()
    
    def on_teeest(self, event):
        self.sender.send(Message(body="aaaaaa"))

reactor = Container(HelloWorld("admin:admin@localhost:32858", "broadcast.user1.rtgQueue"))
events = EventInjector()
reactor.selectable(events) 
thread = threading.Thread(target=reactor.run)
thread.daemon=True
thread.start()

while True:
    line = sys.stdin.readline()
    events.trigger(ApplicationEvent("teeest"))
