#!/usr/bin/env python

# ############################################################################
# Copyright  : (C) 2014 by Teledomic. All rights reserved
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
# Name       :  binding.py
"""
  Summary    : helper for pyqt bindings

wrapper trying to use either PYQt or Pyside if python_qt_binding is installed
otherwise fallback to PyQt
"""
# #############################################################################
from __future__ import absolute_import

__author__    = "Feenes"
__copyright__ = "(C) 2014 by Teledomic. All rights reserved"
__email__     = "info@teledomic.eu"

# -----------------------------------------------------------------------------
#   Imports
# -----------------------------------------------------------------------------
import logging

# -----------------------------------------------------------------------------
#   Globals
# -----------------------------------------------------------------------------
logger = logging.getLogger(__name__)

try:
    from python_qt_binding import QT_BINDING
    from python_qt_binding import QtGui, QtCore
    from python_qt_binding.QtCore import Qt
except:
    QT_BINDING = 'bindingless pyqt'
    from PyQt4 import QtGui, QtCore
    from PyQt4.QtCore import Qt

# Now depending on the binding export some vars
if QT_BINDING == 'pyside':
    import PySide #pylint: disable=F0401
    qt_binding_version_str = PySide.__version__ #pylint: disable=E1101
    qt_binding_version = PySide.__version_info__ # pylint: disable=E1101
    qt_version_str = QtCore.__version__ # pylint: disable=E1101
else:
    qt_binding_version_str = QtCore.PYQT_VERSION_STR
    qt_binding_version = QtCore.PYQT_VERSION
    qt_version_str = QtCore.QT_VERSION_STR
    QtCore.Signal = QtCore.pyqtSignal
    QtCore.Slot = QtCore.pyqtSlot

# -----------------------------------------------------------------------------
#   End of file
# -----------------------------------------------------------------------------
