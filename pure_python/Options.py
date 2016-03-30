#! /usr/bin/python

class Options:
    def __init__(self, hostname="", port="", account_name="", account_public_key="", account_private_key="", broker_public_key="", timeout=60):
        self.hostname = hostname
        self.port = port
        self.accountName = account_name
        self.accountPrivateKey = account_private_key
        self.accountPublicKey = account_public_key
        self.brokerPublicKey = broker_public_key
        self.timeout=timeout
