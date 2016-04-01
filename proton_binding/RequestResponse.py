#!/usr/bin/env python

from __future__ import print_function, unicode_literals
from proton import SSLDomain, Message
from proton.handlers import MessagingHandler
from proton.reactor import Container

from Options import Options

class Requestor(MessagingHandler):
    def __init__(self, opts):
        super(Requestor, self).__init__(prefetch=1000, auto_accept=False, peer_close_is_error=True)
        self.options = opts
        self.address = "amqps://" + self.options.hostname + ":" + str(self.options.port)
        self.request_address = "request." + self.options.accountName
        self.reply_adress = "response/response." + self.options.accountName
        self.response_address = "response." + self.options.accountName
        self.message_counter = 0
        self.request_sent = False

    def on_start(self, event):
        self.container = event.container

        ssl = SSLDomain(SSLDomain.MODE_CLIENT)
        ssl.set_credentials(str(self.options.accountPublicKey), str(self.options.accountPrivateKey), str(""))
        #ssl.set_peer_authentication(SSLDomain.VERIFY_PEER_NAME, trusted_CAs=str(self.options.brokerPublicKey))
        #ssl.set_trusted_ca_db(str(self.options.brokerPublicKey))

        conn = event.container.connect(self.address, ssl_domain=ssl, heartbeat=60000, allowed_mechs=str("EXTERNAL"))
        event.container.create_receiver(conn, self.response_address)
        self.sender = event.container.create_sender(conn, self.request_address)

    def on_sendable(self, event):
        if self.request_sent == False:
            message = Message(body="<FIXML>...</FIXML>", reply_to=self.reply_adress)
            print("-I- Sending request message: " + message.body)
            self.request_sent = True
            self.sender.send(message)
            self.sender.close()

    def on_message(self, event):
        print("-I- Received response message: " + event.message.body)
        self.message_counter += 1
        self.accept(event.delivery)
        event.receiver.close()
        event.connection.close()

class RequestResponse:
    def __init__(self, options):
        self.options = options
        self.message_counter = 0

    def run(self):
        requestor = Requestor(self.options)
        reactor = Container(requestor)
        reactor.run()
        self.message_counter = requestor.message_counter
        print("-I- Received in total " + str(self.message_counter) + " responses")

if __name__ == "__main__":
    hostname = "ecag-fixml-simu1.deutsche-boerse.com"
    port = 10170
    accountName = "ABCFR_ABCFRALMMACC1"
    accountPrivateKey = "ABCFR_ABCFRALMMACC1.pem"
    accountPublicKey = "ABCFR_ABCFRALMMACC1.crt"
    brokerPublicKey = "ecag-fixml-simu1.deutsche-boerse.com.crt"
    timeout = 60

    opts = Options(hostname, port, accountName, accountPublicKey, accountPrivateKey, brokerPublicKey, timeout)
    rr = RequestResponse(opts)
    rr.run()

