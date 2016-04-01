#!/usr/bin/env python

from __future__ import print_function
from proton import Message, SSLDomain, Timeout, ProtonException
from proton.utils import BlockingConnection

from Options import Options


class BlockingBroadcastReceiver:
    capacity = 1000

    def __init__(self, options):
        self.options = options
        self.broadcast_address = "broadcast." + self.options.accountName + ".TradeConfirmation"
        self.address = "amqps://" + self.options.hostname + ":" + str(self.options.port)
        self.message_counter = 0

    def run(self):
        try:
            ssl = SSLDomain(SSLDomain.MODE_CLIENT)
            ssl.set_credentials(str(self.options.accountPublicKey), str(self.options.accountPrivateKey), str(""))

            connection = BlockingConnection(self.address, ssl_domain=ssl, heartbeat=60000)
            receiver = connection.create_receiver(self.broadcast_address, credit=self.capacity)

            while True:
                received_message = None

                try:
                    received_message = receiver.receive(timeout=self.options.timeout)
                except Timeout, e:
                    print("-I- No message received for ", self.options.timeout, " seconds")
                    break

                self.message_counter += 1
                print("-I- Received broadcast message: " + received_message.body)
                receiver.accept()

            print("-I- " + str(self.message_counter) + " messages received")

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

    opts = Options(hostname, port, accountName, accountPublicKey, accountPrivateKey, brokerPublicKey)

    br = BlockingBroadcastReceiver(opts)
    br.run()
