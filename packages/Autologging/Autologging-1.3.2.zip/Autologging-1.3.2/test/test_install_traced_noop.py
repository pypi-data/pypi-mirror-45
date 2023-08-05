# -*- coding: utf-8 -*-

# Copyright (c) 2013, 2015, 2016, 2018, 2019 Matthew Zipay.
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

"""Test case and runner for the :func:`autologging.install_traced_noop`
function.

"""

__author__ = "Matthew Zipay (mattzATninthtestDOTinfo)"

import logging
import unittest

import autologging
from autologging import __version__

# suppress messages to the console
logging.getLogger().setLevel(logging.FATAL + 1)


class InstallTracedNoopTest(unittest.TestCase):
    """Test the :func:`autologging.install_traced_noop` function."""

    def test_installation(self):
        self.assertFalse(autologging.traced is autologging._traced_noop)
        autologging.install_traced_noop()
        self.assertTrue(autologging.traced is autologging._traced_noop)


def suite():
    return unittest.makeSuite(InstallTracedNoopTest)


if __name__ == "__main__":
    unittest.TextTestRunner().run(suite())

