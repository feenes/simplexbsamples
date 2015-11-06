#!/usr/bin/env python

# #############################################################################
# Copyright : (C) 2015 by Teledomic. 
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# Name       :  qtxb.py
"""
Summary    : simple example combining QT and Crossbar.
"""
# #############################################################################
from __future__ import absolute_import

__author__ = "Feenes"
__copyright__ = "(C) 2015 by Teledomic."
__email__     = "info@teledomic.eu"

# -----------------------------------------------------------------------------
#   Imports
# -----------------------------------------------------------------------------
import os
import sys
import argparse
import logging
import time
import threading
from functools import partial

import minibelt
import crossbarconnect


from autobahn.twisted.wamp import ApplicationSession
from twisted.internet import reactor
from twisted.internet import threads

from twisted.internet.defer import inlineCallbacks

# add path to shared python modules to pythonpath
minibelt.add_to_pythonpath('../pylib', starting_point=__file__)

from myapprunner import ApplicationRunner

# setup logging if not used as module
if __name__ == '__main__':
    from xbdemolib.logging import setup_logging
    setup_logging()

from xbdemolib.qt.binding import (
    QtGui, 
    QtCore,
    )

# -----------------------------------------------------------------------------
#   Globals
# -----------------------------------------------------------------------------
logger = logging.getLogger(__name__)

WS_URI = u"ws://localhost:8080/ws"
REALM = u"realm1"
CHAN = "chan1"
RPC_CHAN = "rpc1"

PUBLISH_URL = u"http://localhost:8080/publish"
CALL_URL = u"http://localhost:8080/call"
LP_URL = u"http://localhost:8080/lp"
CGI_URL = u"http://localhost:8080/cgi"

app = None
widget = None
runner = None


stop_request = False

import time

def slow_func(value):
    print("slow %r" % value)
    time.sleep(3)
    print("slow OK")
    return "==" + str(value)

class AppSession(ApplicationSession):
    @inlineCallbacks
    def onJoin(self, details):
        def cb1(value):
            print("CB val %r" % value)
            try:
                widget.sig_subscribe_cb.emit(value)
            except Exception as exc:
                print("EXC %r" % exception)

        def mysum(value):
            print("RPC called val %r" % value)
            if type(value) in [ int, float]:
                return value * value
            elif type(value) in [ str, unicode ]:
                return "**" + value + "**"
            else:
                return "UNKNOWN"

        def slow_done(rslt):
            print("SLOW_DONE_CB %r" % rslt)

        def slow_cb(value):
            #rslt = reactor.callInThread(slow_func, value)
            #print("RSLT = %r" % rslt)
            #slow_func(value)
            d = threads.deferToThread(partial(slow_func, value))
            d.addCallback(slow_done)
            
        
        print("joined %r" % details)
        yield self.subscribe(cb1, CHAN)
        yield self.subscribe(slow_cb, CHAN)
        yield self.register(mysum, RPC_CHAN)


    @inlineCallbacks
    def do_publish(self, data):
        print("do_publish %r" % data)
        rslt = self.publish(CHAN, data)
        yield rslt
        print("pubed %r" % rslt)


def start_xb(options):
    global runner
    """ starts the crossbar.io thread """
    runner = ApplicationRunner(url=WS_URI, realm=REALM)
    runner.run(AppSession)


class MyWidget(QtGui.QWidget):
    """ very basic demo widget """

    sig_subscribe_cb = QtCore.Signal(str)
    sig_quit = QtCore.Signal()

    def __init__(self, parent=None):
        super(MyWidget, self).__init__(parent)
        layout = QtGui.QVBoxLayout(self)
        self.xb_client = crossbarconnect.Client(PUBLISH_URL)

        self.inp1 = QtGui.QLineEdit("enter some text here")
        layout.addWidget(self.inp1)

        self.lab1 = QtGui.QLabel('---')
        layout.addWidget(self.lab1)


        self.btn1 = QtGui.QPushButton("publish event 1")
        layout.addWidget(self.btn1)
        self.btn1.pressed.connect(self._publish)

        self.inp2 = QtGui.QLineEdit("enter another text here")
        layout.addWidget(self.inp2)

        self.btn2 = QtGui.QPushButton("rpc call")
        layout.addWidget(self.btn2)
        self.btn2.pressed.connect(self._call)

        self.btn_quit = QtGui.QPushButton("Quit")
        layout.addWidget(self.btn_quit)
        self.btn_quit.pressed.connect(self._quit)

        logger.debug("now connecting signals")
        self.sig_subscribe_cb.connect(self.subscribe_callback)
        self.sig_quit.connect(self._quit)

        logger.info("widget created")

    def _get_session(self):
        if runner:
            return runner.session
        return None

    def _quit(self):
        logger.info("will close window")
        self.close()

    def _publish(self):
        msg = self.inp1.text()
    
        #logger.info("shall publish via xb connect")
        #self.xb_client.publish(CHAN, msg)

        logger.info("shall publish via xb connect")
        session = self._get_session()
        rslt = reactor.callFromThread(session.do_publish, msg)
        print("REACTCALLRSLT %r" % rslt)

    def _call(self):
        logger.info("will do a blocking XB-RPC call")

    @QtCore.Slot(str)
    def subscribe_callback(self, value):
        logger.info("handling subscribe callback %r", value)
        self.lab1.setText(value)

    def handle_rpc_call(self):
        logger.info("handling an rpc call")
        return 3


def mk_parser():
    """ creates commandline parser 
        even the lousiest program shall have
        a -h switch
    """
    description="simple qtxb test case"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--cli", "-c", action='store_true',
        help="starts a CLI for debugging")
    return parser
    

def main():
    global app
    global widget
    global session

    args = sys.argv[1:]
    parser = mk_parser()
    options = parser.parse_args(args)

    xb_thrd = threading.Thread(target=start_xb, args=[options])
    xb_thrd.daemon = True
    xb_thrd.start()

    
    # create QT widgets
    time.sleep(4)
    print("will now create app and widget")
    app = QtGui.QApplication(sys.argv)
    widget = MyWidget()

    if options.cli:
        from xbdemolib.cli import CLI

        namespace = dict(
            args=args,
            options=options,
            app=app,
            widget=widget,
            runner=runner,
        )
        cli = CLI(options, 
                namespace=namespace, 
                quit_func=widget.sig_quit.emit)
        cli.run_as_thread(daemon=False)

    #time.sleep(4)
    print("will now show widget")
    widget.show() 

    #time.sleep(4)
    print("will now start main loop")
    rslt = app.exec_() # start QT event loop
    app = None
    sys.exit(rslt) # start QT event loop


if __name__ == '__main__':
    main()
# -----------------------------------------------------------------------------
#   End of file
# -----------------------------------------------------------------------------

