# -*- coding: utf-8 -*-
from __future__ import print_function

import unittest
from sphinx_testing import TestApp


class TestNode(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = TestApp(buildername='singlehtml',
                          srcdir='tests/doc/node_default_conf')
        cls.app.build()

    def test(self):
        pass
