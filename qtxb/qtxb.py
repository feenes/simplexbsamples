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
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
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

import threading

import minibelt
import crossbarconnect

# add path to shared python modules to pythonpath
minibelt.add_to_pythonpath('../pylib', starting_point=__file__)

# setup logging
from xbdemolib.logging import setup_logging
setup_logging()

from xbdemolib.qt.binding import (
    QtGui, 
    QtCore,
    )

import logging
import time

# -----------------------------------------------------------------------------
#   Globals
# -----------------------------------------------------------------------------
logger = logging.getLogger(__name__)

stop_request = False

def start_xb(options):
    """ starts the crossbar.io thread """
    global stop_request
    print("that will be XB")
    while not stop_request:
        print("XB.")
        time.sleep(10)
    print("XB END")



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
    

class MyWidget(QtGui.QWidget):
    """ very basic demo widget """

    sig_subscribe_cb = QtCore.Signal(str)
    sig_quit = QtCore.Signal()

    def __init__(self, parent=None):
        super(MyWidget, self).__init__(parent)
        layout = QtGui.QVBoxLayout(self)

        self.inp1 = QtGui.QLineEdit("enter some text here")
        layout.addWidget(self.inp1)

        self.btn1 = QtGui.QPushButton("publish event 1")
        layout.addWidget(self.btn1)
        self.btn1.pressed.connect(self._publish)

        self.inp1 = QtGui.QLineEdit("enter another text here")
        layout.addWidget(self.inp1)

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

    def _quit(self):
        logger.info("will close window")
        self.close()

    def _publish(self):
        logger.info("shall publish via xb")

    def _call(self):
        logger.info("will do a blocking XB-RPC call")

    @QtCore.Slot(str)
    def subscribe_callback(self, value):
        logger.info("handling subscribe callback %r", value)

    def handle_rpc_call(self):
        logger.info("handling an rpc call")
        return 3


def main():
    args = sys.argv[1:]
    parser = mk_parser()
    options = parser.parse_args(args)

    xb_thrd = threading.Thread(target=start_xb, args=[options])
    xb_thrd.daemon = True
    xb_thrd.start()
    
    app = QtGui.QApplication(sys.argv)
    widget = MyWidget()

    if options.cli:
        from xbdemolib.cli import CLI

        namespace = dict(
            args=args,
            options=options,
            app=app,
            widget=widget,
        )
        cli = CLI(options, 
                namespace=namespace, 
                quit_func=widget.sig_quit.emit)
        cli.run_as_thread(daemon=False)

    widget.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
# -----------------------------------------------------------------------------
#   End of file
# -----------------------------------------------------------------------------

