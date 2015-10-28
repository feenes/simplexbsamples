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
# Name       :  logging.py
"""
Summary    : helper to setup logging
"""
# #############################################################################
from __future__ import absolute_import

__author__ = "Feenes"
__copyright__ = "(C) 2015 by Teledomic."
__email__     = "info@teledomic.eu"


import os
import sys
import json
import logging

import minibelt


def setup_logging(name=''):
    """ sets up logging 
        if name is None, then a null logger will be configured
        otherwise a default logger will be set up
    """

    log_config = os.environ.get('LOG_CONFIG', name)

    # is no logging desired ?
    if log_config is None or log_config.lower() is 'none': 
        logger = logging.getLogger('')
        logger.addHandler(logging.NullHandler())
        return

    if os.path.isfile(log_config): # found a log config file?
        suffix = os.path.splitext(log_config)[1].lower()
        if suffix in ['.ini', '.conf']:
            logging.config.fileConfig(log_config)
        elif suffix == '.json':
            with open(log_config) as fin:
                cfg = json.load(fin)
                logging.config.dictConfig(cfg)
        return

    try: # can I find a log config module ?
        cfg_module = minibelt.import_from_path(log_config)
        if hasattr(cfg_module, 'setup_logging'):
            cfg_module.setup_logging()
    except:
        # basic logging of warnings to stderr?
        logging.basicConfig(
            stream=sys.stdout,
            #level=logging.WARNING,
            level=logging.INFO,
            format="%(asctime)s %(levelname)-8s %(name)7s: %(message)s",
            datefmt="%H:%M:%S",
            )

pass
