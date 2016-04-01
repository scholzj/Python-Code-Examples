from __future__ import print_function, unicode_literals
import sys
import threading
from proton import Message, SSLDomain
from proton.handlers import MessagingHandler, TransactionHandler
from proton.reactor import ApplicationEvent, Container, EventInjector

class BroadcastReceiver(MessagingHandler):
    def __init__(self, server, address):
        super(BroadcastReceiver, self).__init__()
        self.server = server
        self.address = address

    def on_start(self, event):
        self.container = event.container

        ssl = SSLDomain(SSLDomain.MODE_CLIENT)
        ssl.set_credentials(str("../tests/resources/local/ABCFR_ABCFRALMMACC1.crt"), str("../tests/resources/local/ABCFR_ABCFRALMMACC1.pem"), str(""))
        #ssl.set_peer_authentication(SSLDomain.VERIFY_PEER_NAME, trusted_CAs=str("../tests/resources/local/cbgc01.crt"))
        #ssl.set_trusted_ca_db(str("../tests/resources/local/cbgc01.crt"))

        conn = event.container.connect(self.server, ssl_domain=ssl, allowed_mechs=str("EXTERNAL"))
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

reactor = Container(BroadcastReceiver("amqps://cbgc01.xeop.de:19700", "broadcast.ABCFR_ABCFRALMMACC1.TradeConfirmation"))
events = EventInjector()
reactor.selectable(events) 
thread = threading.Thread(target=reactor.run)
thread.daemon=True
thread.start()

while True:
    line = sys.stdin.readline()
    events.trigger(ApplicationEvent("teeest"))
