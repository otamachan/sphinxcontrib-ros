# -*- coding: utf-8 -*-
from __future__ import print_function

import unittest
from sphinx_testing import TestApp


class TestSyntaxHighlight(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = TestApp(buildername='singlehtml',
                          srcdir='tests/doc/syntax_highlight',
                          copy_srcdir_to_tmpdir=True)
        cls.app.build()

    def test(self):
        pass
