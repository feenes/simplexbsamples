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

import minibelt

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
    mk_xb = os.path.join(TOP_DIR, 'xb', 'mkxb.py')
    return run_py([mk_xb])

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

if __name__ == '__main__':
    main()
# -----------------------------------------------------------------------------
#   End of file
# -----------------------------------------------------------------------------
