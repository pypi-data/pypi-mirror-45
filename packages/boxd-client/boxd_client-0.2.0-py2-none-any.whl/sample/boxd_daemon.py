#!/usr/bin/env python3

from __future__ import print_function
from __future__ import absolute_import

import threading

from boxd_client.proto import web_pb2 as web
from boxd_client.boxd_client import BoxdClient

class BoxdDaemon(threading.Thread):


    def __init__(self, box_client, handler):
        self._web_stub = box_client.web_stub
        self._handler = handler
        threading.Thread.__init__(self)

    def run(self):
        self.listen_and_read_new_block(handler=self._handler)


    def listen_and_read_new_block(self, handler):
        blocks = self._web_stub.ListenAndReadNewBlock(web.ListenBlocksReq())
        try:
            for block in blocks:
                #print (r["height"])
                handler(block)
        except:
            pass

def block_handler(block):
    print (block)

boxd_client = BoxdClient("39.105.214.10", 19161)
boxd_daemon = BoxdDaemon(boxd_client, block_handler)
boxd_daemon.start()