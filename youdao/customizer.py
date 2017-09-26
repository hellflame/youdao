# coding=utf8
"""
    fetch result from the backup server, default backup server hellflame.net:3679
    btw: customized server is not a must, but it will speed up a little the query progress
"""

import socket
import json
from contextlib import contextmanager
__author__ = "hellflame"


class Customize(object):
    def __init__(self, target, host='hellflame.net', port=3697):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(7)
        self.target = target
        self.address = (host, port)

    @contextmanager
    def connection(self):
        try:
            self.socket.connect(self.address)
            self.socket.send(self.target.replace('\r\n', '') + b'\r\n')
            # just make this an easy way
            yield self.socket.recv(100000)
            self.socket.close()
        except Exception:
            yield ''

    def server_fetch(self):
        with self.connection() as result:
            if result:
                return json.loads(result)
            return None


if __name__ == '__main__':
    Customize('localhost', 'localhost', 5001).server_fetch()




