"""
"""
# coding=utf-8


import unittest
import mock

from InvokeDockerFlow.flow import Flow


class FlowTests(unittest.TestCase):
    """
    Tests for Flow
    """

    def setUp(self):
        """
        """
        self.flow = Flow()
