#!/usr/bin/env python

import unittest

from pure_python.Options import Options
from pure_python.BroadcastReceiver import BroadcastReceiver
from pure_python.RequestResponse import RequestResponse

from utils.Responder import Responder

from qpid.messaging import *


class PurePythonTests(unittest.TestCase):
    def setUp(self):
        hostname = "ecag-fixml-dev1"
        port = 35671
        accountName = "ABCFR_ABCFRALMMACC1"
        accountPrivateKey = "./tests/resources/ABCFR_ABCFRALMMACC1.pem"
        accountPublicKey = "./tests/resources/ABCFR_ABCFRALMMACC1.crt"
        brokerPublicKey = "./tests/resources/ecag-fixml-dev1.crt"
        self.options = Options(hostname, port, accountName, accountPublicKey, accountPrivateKey, brokerPublicKey, timeout=5)

    def test_broadcastReceiver(self):
        connection = Connection(host=self.options.hostname, port=35672,
                                username="admin", password="admin", heartbeat=60)
        connection.open()
        session = connection.session()
        sender = session.sender("broadcast/broadcast.ABCFR.TradeConfirmation; { node: { type: topic }, assert: never }")
        sender.send(Message("<FIXML>...</FIXML>", durable=True), sync=True);
        connection.close();

        br = BroadcastReceiver(self.options)
        br.run()

        self.assertGreaterEqual(br.message_counter, 1)


    def test_requestResponse(self):
        responder = Responder(self.options.hostname, 35672, "admin", "admin", "request_be.ABCFR_ABCFRALMMACC1.EUREX", 5)
        responder.start()

        rr = RequestResponse(self.options)
        rr.run()

        self.assertGreaterEqual(rr.message_counter, 1)

if __name__ == '__main__':
    unittest.main()