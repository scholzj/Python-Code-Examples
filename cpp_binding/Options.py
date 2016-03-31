#! /usr/bin/python

class Options:
    def __init__(self, hostname="", port="", account_name="", timeout=60):
        self.hostname = hostname
        self.port = port
        self.accountName = account_name
        self.timeout=timeout
