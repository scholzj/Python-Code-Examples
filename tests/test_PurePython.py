import unittest

from pure_python.Options import Options
from pure_python.BroadcastReceiver import BroadcastReceiver

from qpid.messaging import *

class PurePythonTests(unittest.TestCase):
    def setUp(self):
        hostname = "cbgc01"
        port = 19700
        accountName = "ABCFR_ABCFRALMMACC1"
        accountPrivateKey = "./tests/resources/ABCFR_ABCFRALMMACC1.pem"
        accountPublicKey = "./tests/resources/ABCFR_ABCFRALMMACC1.crt"
        brokerPublicKey = "./tests/resources/cbgc01.crt"
        self.options = Options(hostname, port, accountName, accountPublicKey, accountPrivateKey, brokerPublicKey, timeout=5)

    def test_broadcastReceiver(self):
        connection = Connection(host=self.options.hostname, port=29700,
                                username="admin", password="admin", heartbeat=60)
        connection.open()
        session = connection.session()
        sender = session.sender("broadcast/broadcast.ABCFR.TradeConfirmation; { node: { type: topic }, assert: never }")
        sender.send(Message("<FIXML>...</FIXML>", durable=True), sync=True);
        connection.close();

        br = BroadcastReceiver(self.options)
        br.run()

        self.assertGreaterEqual(br.message_counter, 1)

if __name__ == '__main__':
    unittest.main()