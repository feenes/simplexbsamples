#!/usr/bin/env python

from autobahn.twisted.wamp import ApplicationRunner
from autobahn.twisted.wamp import ApplicationSession
import threading

WS_URI = u"ws://localhost:8080/ws"
REALM = u"realm1"

class AppSession(ApplicationSession):
    def onJoin(self, details):
        print("joined %r" % details)

def start_xb():
    """ starts the crossbar.io thread """
    runner = ApplicationRunner(url=WS_URI, realm=REALM)
    runner.run(AppSession)

xb_thrd = threading.Thread(target=start_xb)
xb_thrd.start()

