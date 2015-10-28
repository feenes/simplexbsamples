
#!/usr/bin/env python

# ############################################################################
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
# Name       : cli.py
"""
  Summary    :  simple ipython debug CLI (if ipython is installed)

"""
# #############################################################################
from __future__ import absolute_import
from __future__ import print_function

__author__ = "Feenes"
__copyright__ = "(C) 2015 by Teledomic."
__email__     = "info@teledomic.eu"

# -----------------------------------------------------------------------------
#   Imports
# -----------------------------------------------------------------------------
import threading
import logging

import readline

from six.moves import input

# -----------------------------------------------------------------------------
#   Globals
# -----------------------------------------------------------------------------
logger = logging.getLogger(__name__)


class CLI(object):
    input_func = input

    def __init__(self, options=None, namespace=None, quit_func=None):
        cls = self.__class__
        self._cli_thread = None
        self._options = options
        if namespace is None:
            namespace = dict(__lock=threading.Lock())
        self.namespace = namespace
        if not hasattr(namespace, '__lock'):
            namespace.update(dict(__lock=threading.Lock()))
        self._lock = namespace['__lock']
        self._quit_function = quit_func

    def set_quit_function(self, func):
        self._quit_function = func

    def run(self):
        """ allows to run an ipython shell with the CLI's context vars """
        namespace = self.namespace
        try:
            from IPython.terminal.embed import InteractiveShellEmbed
            use_ipython = True
        except ImportError:
            use_ipython = False
            
        if use_ipython:
            shell = InteractiveShellEmbed(user_ns=namespace)
            shell()
        else:
            self.mini_shell(namespace=namespace)

        if self._quit_function:
            try:
                self._quit_function(self)
            except TypeError:
                logger.warning("using obsolete quit function without argument")
                self._quit_function()

    def mini_shell(self, namespace):
        """ Rather lousy Python shell for debugging.
            Just in case ipython is not installed or has the wrong version
        """
        print("Did not find an apropriate version of ipython")
        print("will start therefore just a rather basic CLI without tab expansion")

        while True:
            cmd_line = self.input_func('-->')
            upper_stripped = cmd_line.strip().upper()
            shall_quit = (upper_stripped == 'Q' or upper_stripped == 'QUIT')
            if shall_quit:
                break
            try:
                eval(compile(cmd_line, '<string>', 'single'), namespace) # pylint: disable=W0122,C0301
            except Exception as exc: # pylint: disable=W0703
                logger.error('ERROR: %r' % exc)

        print("END OF CLI")
        self.write_history()

    def write_history(self, fname=None):
        pass

    def run_as_thread(self, name='cli', daemon=True):
        """ start CLI as a thread
            This is needed for Qt Apps, where the GUI must be called in the main thread
        """
        self._cli_thread = cli_thread = threading.Thread(target=self.run, 
            name=name)
        cli_thread.daemon = daemon 
        cli_thread.start()

# -----------------------------------------------------------------------------
#   End of file
# -----------------------------------------------------------------------------
