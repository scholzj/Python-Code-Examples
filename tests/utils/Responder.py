import threading
from qpid.messaging import *

class Responder(threading.Thread):
    def __init__(self, hostname, port, username, password, request_queue, timeout=60):
        threading.Thread.__init__(self)
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.request_address = request_queue + "; { node: { type: queue }, assert: never, mode: consume }"
        self.timeout = timeout

    def run(self):
        try:
            connection = Connection(host=self.hostname, port=self.port,
                                    username=self.username, password=self.password, heartbeat=60)

            connection.open()
            session = connection.session()

            try:
                receiver = session.receiver(self.request_address)
                message = receiver.fetch(timeout=self.timeout)
                print "-I- Received request with content: ", message.content

                sender = session.sender(message.reply_to)
                sender.send(Message("Responding to " + message.content, durable=False), sync=True)
                print "-I- Response sent"

                session.acknowledge()
            except Empty, e:
                print "-I- No request received for ", self.timeout, " seconds"

            connection.close();

        except MessagingError, m:
            print "-E- Caught exception in responder: ", m
            raise m
