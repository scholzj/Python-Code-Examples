from qpid.messaging import *

class Broadcaster():
    def __init__(self, hostname, port, username, password, exchange, routing_key, count=1):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.broadcast_address = exchange + "/" + routing_key + "; { node: { type: topic }, assert: never }"
        self.count = count

    def run(self):
        try:
            connection = Connection(host=self.options.hostname, port=35672,
                                    username="admin", password="admin", heartbeat=60)
            connection.open()
            session = connection.session()
            sender = session.sender(self.broadcast_address)

            for i in range(0, 0 + self.count):  # to iterate between 10 to 20
                sender.send(Message("<FIXML>" + str(i) + "</FIXML>", durable=True), sync=True);
            else:  # else part of the loop
                print "Broadcaster sent ", self.count, " messages"

            connection.close();
        except MessagingError, m:
            print "-E- Caught exception in broadcaster: ", m
            raise m
