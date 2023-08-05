#!/usr/bin/env python3
# vim: set fenc=utf8 ts=4 sw=4 et :
from shutil import rmtree
from tempfile import mkdtemp
import unittest

from pdml2flow.conf import Conf
from pdml2flow.flow import Flow

class TestCase(unittest.TestCase):
    """Class used as base object for all tests
    This class ensures that the global configruation object is always reset
    between tests
    """

    def setUp(self):
        # save
        self.__conf = Conf.get()

    def tearDown(self):
        # reset
        Conf.set(self.__conf)
        Flow.newest_overall_frame_time = 0

class TestCaseWithTestDir(TestCase):

    def setUp(self):
        super().setUp()
        self.test_dir = mkdtemp()

    def tearDown(self):
        rmtree(self.test_dir)
        super().tearDown()
