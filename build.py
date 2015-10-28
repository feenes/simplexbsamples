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
# Name       :  template.py
"""
Summary    :
"""
# #############################################################################
from __future__ import absolute_import
from __future__ import print_function

__author__    = "Feenes"
__copyright__ = "(C) 2015 by Teledomic. All rights reserved"
__email__     = "info@teledomic.eu"
# #############################################################################


# -----------------------------------------------------------------------------
#   Imports
# -----------------------------------------------------------------------------
import os
import sys

import argparse
import logging
import subprocess

import minibelt

TOP_DIR = os.path.realpath(os.path.dirname(__file__))

# add path to shared python modules to pythonpath
minibelt.add_to_pythonpath('pylib', starting_point=__file__)

# setup logging if not used as module
if __name__ == '__main__':
    from xbdemolib.logging import setup_logging
    setup_logging()

# -----------------------------------------------------------------------------
#   Globals
# -----------------------------------------------------------------------------
logger = logging.getLogger(__name__)

def mk_xb():
    xb_dir = os.path.join(TOP_DIR, 'xb')
    print('-' * 78)
    print("compiling xb configurations")
    for bdir, dirs, files in os.walk(xb_dir):
        if not '.crossbar' in dirs:
            continue
        print("XBDIR %r" % bdir)

def compile_coffee():
    js_dir = os.path.join(TOP_DIR, 'js')
    print('-' * 78)
    print("compiling js configurations")
    for bdir, dirs, files in os.walk(js_dir):
        for fname in files:
            if not os.path.splitext(fname)[1].lower() == '.coffee':
                continue
            full_path = os.path.join(bdir, fname)
            print("compile %r" % full_path)
            rslt = subprocess.call(['coffee', '-c', '-m', full_path])
            print("RSLT %r" % rslt)
        

def mk_parser():
    """ creates commandline parser 
        even the lousiest program shall have
        a -h switch
    """
    description="simple builder. (builds by default xb-cfg)"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--cli", "-c", action='store_true',
        help="starts a CLI for debugging")
    parser.add_argument("--coffee", "-C", action='store_true',
        help="compiles all coffeescripts",
        )
    parser.add_argument("--all", "-a", action='store_true',
        help="compiles all ite,s",
        )
    return parser
    

def main():
    args = sys.argv[1:]
    parser = mk_parser()
    options = parser.parse_args(args)
    
    if options.cli:
        from xbdemolib.cli import CLI
        namespace = dict(
            args=args,
            options=options,
        )
        cli = CLI(options, namespace=namespace)
        cli.run_as_thread(daemon=False)

    mk_xb()
    if options.coffee or options.all:
        compile_coffee()

if __name__ == '__main__':
    main()
# -----------------------------------------------------------------------------
#   End of file
# -----------------------------------------------------------------------------
