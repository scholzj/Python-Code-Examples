#! /usr/bin/python

from Options import Options
from qpid.messaging import *


# Uncomment the following lines to enable protocol logging
# from qpid.log import enable, DEBUG
# enable("qpid", DEBUG)

class RequestResponse:
    timeout = 60

    def __init__(self, options):
        self.options = options
        self.request_address = "request." + self.options.accountName + "/request; " \
                               "{ node: { type: topic }, create: never }"
        self.reply_adress = "response/response." + self.options.accountName + ".response_queue_1; " \
                            "{ create: receiver, node: { type: topic } }"
        self.response_address = "response." + self.options.accountName + ".response_queue_1; {create: receiver, " \
                                "assert: never, node: { type: queue, x-declare: { auto-delete: true, exclusive: false, " \
                                "arguments: {'qpid.policy_type': ring, 'qpid.max_count': 1000, 'qpid.max_size': 1000000}}, " \
                                "x-bindings: [{exchange: 'response', queue: 'response." + self.options.accountName + ".response_queue_1', " \
                                "key: 'response." + self.options.accountName + ".response_queue_1'}]}}";

    def run(self):
        try:
            connection = Connection(host=self.options.hostname, port=self.options.port,
                                username=self.options.accountName, sasl_mechanisms="EXTERNAL", transport="ssl",
                                ssl_keyfile=self.options.accountPrivateKey, ssl_certfile=self.options.accountPublicKey,
                                ssl_trustfile=self.options.brokerPublicKey, heartbeat=60)
            connection.open()
            session = connection.session()
            receiver = session.receiver(self.response_address)
            sender = session.sender(self.request_address)

            message = Message("<FIXML>...</FIXML>", durable=False, reply_to=self.reply_adress)
            sender.send(message, sync=True);

            try:
                message = receiver.fetch(timeout=self.timeout)
                session.acknowledge(sync=False)

                print "-I- Response received with content: ", message.content

            except Empty:
                print "-I- No response received for ", self.timeout, " seconds"

            session.sync(timeout=None)

            sender.close()
            receiver.close()
            session.close()
            connection.close()
        except MessagingError, m:
            print "-E- Caught exception: ", m

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

rr = RequestResponse(opts)
rr.run()
