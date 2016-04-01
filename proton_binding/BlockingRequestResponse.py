#!/usr/bin/env python

from __future__ import print_function
from proton import Message, SSLDomain, Timeout, ProtonException
from proton.utils import BlockingConnection

from Options import Options


class BlockingRequestResponse:
    def __init__(self, options):
        self.options = options
        self.request_address = "request." + self.options.accountName
        self.reply_adress = "response/response." + self.options.accountName
        self.response_address = "response." + self.options.accountName
        self.address = "amqps://" + self.options.hostname + ":" + str(self.options.port)
        self.message_counter = 0

    def run(self):
        try:
            ssl = SSLDomain(SSLDomain.MODE_CLIENT)
            ssl.set_credentials(str(self.options.accountPublicKey), str(self.options.accountPrivateKey), str(""))

            connection = BlockingConnection(self.address, ssl_domain=ssl, heartbeat=60000)
            receiver = connection.create_receiver(self.response_address)
            sender = connection.create_sender(self.request_address)

            message = Message(body="<FIXML>...</FIXML>", reply_to=self.reply_adress)
            print("-I- Sending request message: " + message.body)
            sender.send(message);

            try:
                received_message = receiver.receive(timeout=self.options.timeout)
                print("-I- Received response message: " + received_message.body)
                self.message_counter += 1
                receiver.accept()
            except Timeout, e:
                print("-I- No message received for ", self.options.timeout, " seconds")

            connection.close()
        except ProtonException, e:
            print("-E- Caught exception: " + str(e))

if __name__ == "__main__":
    hostname = "ecag-fixml-simu1.deutsche-boerse.com"
    port = 10170
    accountName = "ABCFR_ABCFRALMMACC1"
    accountPrivateKey = "ABCFR_ABCFRALMMACC1.pem"
    accountPublicKey = "ABCFR_ABCFRALMMACC1.crt"
    brokerPublicKey = "ecag-fixml-simu1.deutsche-boerse.com.crt"
    timeout = 60

    hostname = "cbgc01.xeop.de"
    port = 19700
    accountName = "ABCFR_ABCFRALMMACC1"
    accountPrivateKey = "../tests/resources/local/ABCFR_ABCFRALMMACC1.pem"
    accountPublicKey = "../tests/resources/local/ABCFR_ABCFRALMMACC1.crt"
    brokerPublicKey = "../tests/resources/local/cbgc01.crt"

    opts = Options(hostname, port, accountName, accountPublicKey, accountPrivateKey, brokerPublicKey, timeout)
    rr = BlockingRequestResponse(opts)
    rr.run()
