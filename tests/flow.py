"""
"""
# coding=utf-8


import unittest
import mock

import sys
print(sys.modules)

# sys.modules['InvokeDockerFlow.utils'] = mock.Mock(return_value=)


from invoke_docker_flow.flow import Flow


class FlowTests(unittest.TestCase):
    """
    Tests for Flow
    """

    def setUp(self):
        """
        """
        self.flow = Flow(
            "vjftw/invoke-docker-flow"
        )

    def test_get_development_container_name(self):
        pass
