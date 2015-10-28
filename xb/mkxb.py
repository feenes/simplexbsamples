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
# Name       :  mkxb.py
"""
Summary    : converts an xb template file to a crossbar configuration
"""
# #############################################################################
from __future__ import absolute_import
from __future__ import print_function

__author__    = "Feenes"
__copyright__ = "(C) 2015 by Teledomic. All rights reserved"
__email__     = "info@teledomic.eu"
# #############################################################################

import os
import sys
import json
import argparse
from collections import OrderedDict

# -----------------------------------------------------------------------------
#   Globals
# -----------------------------------------------------------------------------
MY_DIR = os.path.realpath(os.path.dirname(__file__))

def is_windows():
    return sys.platform == 'win32'

def escaped(val):
    """ escapes a string to allow injecting it into a json conf """
    val = val.replace('\\',  '/')
    val = val.replace('"', '\"')
    return val

def make_xb_cfg(silent=False, xbdir=''):
    xbcfg_fmt = os.path.join(xbdir, ".crossbar" , "%sconfig.json")
    src = xbcfg_fmt % "tmpl_"
    dst = xbcfg_fmt % ""
    
    if not silent:
        print(repr(src), repr(dst)) 
    
    lines = []

    fields = dict(
        PYTHON=escaped(sys.executable),
        TOP_DIR=escaped(MY_DIR),
    )
    
    with open(src, "r") as fin:
        for line in fin:
            strline = line.strip()
            if strline.startswith("#"):
                continue
            for key, val in fields.items():
                keystr = "$$$"+key+"$$$"
                line = line.replace(keystr, val)
            lines.append(line)

    full_txt = ('\n'.join(lines))
    #print("FT:\n", full_txt)
    data = json.JSONDecoder(object_pairs_hook=OrderedDict).decode(full_txt)

    if is_windows:
        if 'manhole' in data['workers'][0]:
            del data['workers'][0]['manhole']
            print("remove manhole")

    with open(dst, "w") as fout:
        json.dump(data, fout, indent=2)

def mk_parser():
    """ creates commandline parser 
        even the lousiest program shall have
        a -h switch
    """
    description="simple qtxb test case"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("xbdir", nargs='*',
        help="CLI for debugging")
    return parser

def main():
    args = sys.argv[1:]
    parser = mk_parser()
    options = parser.parse_args(args)
    xbdirs = options.xbdir
    print("XBDIRS %r" % (xbdirs,) )
    if not xbdirs:
        xbdirs = [ os.path.join(MY_DIR, 'xb_simple') ]
        print("XBDIRS %r" % (xbdirs,) )

    for xbdir in xbdirs:
        print("make xb config file for %r" % xbdir)
        make_xb_cfg(xbdir=xbdir)

if __name__ == "__main__":
    main()
