#!/usr/bin/env python

import unittest

from cpp_binding.Options import Options
from cpp_binding.BroadcastReceiver import BroadcastReceiver
from cpp_binding.RequestResponse import RequestResponse
from cpp_binding.Amqp10BroadcastReceiver import Amqp10BroadcastReceiver
from cpp_binding.Amqp10RequestResponse import Amqp10RequestResponse

from utils.Responder import Responder

from qpid.messaging import *


class CppBindingTests(unittest.TestCase):
    def setUp(self):
        hostname = "ecag-fixml-dev1"
        port = 35671
        accountName = "ABCFR_ABCFRALMMACC1"
        self.options = Options(hostname, port, accountName, timeout=5)

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

    def test_amqp10BroadcastReceiver(self):
        connection = Connection(host=self.options.hostname, port=35672,
                                username="admin", password="admin", heartbeat=60)
        connection.open()
        session = connection.session()
        sender = session.sender("broadcast/broadcast.ABCFR.TradeConfirmation; { node: { type: topic }, assert: never }")
        sender.send(Message("<FIXML>...</FIXML>", durable=True), sync=True);
        connection.close();

        br = Amqp10BroadcastReceiver(self.options)
        br.run()

        self.assertGreaterEqual(br.message_counter, 1)

    def test_amqp10RequestResponse(self):
        responder = Responder(self.options.hostname, 35672, "admin", "admin", "request_be.ABCFR_ABCFRALMMACC1.EUREX", 5)
        responder.start()

        rr = Amqp10RequestResponse(self.options)
        rr.run()

        self.assertGreaterEqual(rr.message_counter, 1)

if __name__ == '__main__':
    unittest.main()