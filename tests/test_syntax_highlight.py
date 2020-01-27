# -*- coding: utf-8 -*-
from __future__ import print_function

import unittest
from sphinx_testing import TestApp as _TestApp


class TestSyntaxHighlight(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = _TestApp(buildername='singlehtml',
                           srcdir='tests/doc/syntax_highlight',
                           copy_srcdir_to_tmpdir=True)

    def test(self):
        self.app.build()
