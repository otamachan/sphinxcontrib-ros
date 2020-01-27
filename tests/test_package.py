# -*- coding: utf-8 -*-
from __future__ import print_function

import unittest
from sphinx_testing import TestApp as _TestApp


class TestPackage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = _TestApp(buildername='singlehtml',
                           srcdir='tests/doc/package_default_conf')

    def test(self):
        self.app.build()


class TestPackageCustomizedConf(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = _TestApp(buildername='singlehtml',
                           srcdir='tests/doc/package_customized_conf')

    def test(self):
        self.app.build()
