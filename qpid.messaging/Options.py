#! /usr/bin/python

class Options:
    def __init__(self, hostname="", port="", accountName="", accountPublicKey="", accountPrivateKey="", brokerPublicKey=""):
        self.hostname = hostname
        self.port = port
        self.accountName = accountName
        self.accountPrivateKey = accountPrivateKey
        self.accountPublicKey = accountPublicKey
        self.brokerPublicKey = brokerPublicKey