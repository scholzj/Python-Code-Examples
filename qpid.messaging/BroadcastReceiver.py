#! /usr/bin/python

from Options import Options
from qpid.messaging import *

# Uncomment the following lines to enable protocol logging
# from qpid.log import enable, DEBUG
# enable("qpid", DEBUG)

class BroadcastReceiver:
    timeout = 60
    block_size = 100
    capacity = 1000

    def __init__(self, options):
        self.options = options
        self.broadcast_address = "broadcast." + self.options.accountName + ".TradeConfirmation; " \
                                 "{ node: { type: queue } , create: never , mode: consume , assert: never }"

    def run(self):
        message_counter = 0

        try:
            connection = Connection(host=self.options.hostname, port=self.options.port,
                                    username=self.options.accountName, sasl_mechanisms="EXTERNAL", transport="ssl",
                                    ssl_keyfile=self.options.accountPrivateKey, ssl_certfile=self.options.accountPublicKey,
                                    ssl_trustfile=self.options.brokerPublicKey, heartbeat=60)
            connection.open()
            session = connection.session()
            receiver = session.receiver(self.broadcast_address)
            receiver.capacity = self.capacity

            while True:
                received_message = None

                try:
                    received_message = receiver.fetch(timeout=self.timeout)
                except Empty:
                    session.acknowledge(sync=True)
                    print "-I- No message received for ", self.timeout, " seconds"
                    break

                message_counter += 1
                print "-I- Received message containing: ", received_message.content

                if message_counter % self.block_size == 0:
                    session.acknowledge(sync=True)

            print "-I- ", message_counter, " messages received"

            receiver.close()
            session.close()
            connection.close()
        except MessagingError, m:
            print "Caught exception: ", m


hostname = "ecag-fixml-simu1.deutsche-boerse.com"
port = 10170
accountName = "ABCFR_ABCFRALMMACC1"
accountPrivateKey = "ABCFR_ABCFRALMMACC1.pem"
accountPublicKey = "ABCFR_ABCFRALMMACC1.crt"
brokerPublicKey = "ecag-fixml-simu1.deutsche-boerse.com.crt"

hostname = "cbgc01"
port = 19700
accountName = "ABCFR_ABCFRALMMACC1"
accountPrivateKey = "ABCFR_ABCFRALMMACC1.pem"
accountPublicKey = "ABCFR_ABCFRALMMACC1.crt"
brokerPublicKey = "cbgc01.crt"

opts = Options(hostname, port, accountName, accountPublicKey, accountPrivateKey, brokerPublicKey)

br = BroadcastReceiver(opts)
br.run()
