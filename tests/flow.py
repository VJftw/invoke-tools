"""
Flow tests
"""
# coding=utf-8

import unittest
import mock

import sys

utils_mock = mock.Mock()
utils_mock.Utils.get_branch.return_value = "master"
utils_mock.Utils.get_version.return_value = "1.0.0"
sys.modules['idflow.utils'] = utils_mock

from idflow import Flow


class FlowTests(unittest.TestCase):
    """
    Tests for Flow
    """

    def test_init(self):
        """
        Flow: Should correctly intialise
        """
        flow = Flow(
            "vjftw/invoke-docker-flow",
            "tool",
            "branch",
            "version"
        )
        self.assertEqual(flow.get_repository(),
                         "vjftw/invoke-docker-flow")
        self.assertEqual(flow.get_prefix(),
                         "tool")
        self.assertEqual(flow.get_branch(),
                         "branch")
        self.assertEqual(flow.get_version(),
                         "version")

    def test_get_development_container_name(self):
        """
        Flow: Should return the development container name
        """
        flow = Flow(
            "vjftw/invoke-docker-flow"
        )
        self.assertEqual(
            flow.get_development_container_name(),
            "vjftw/invoke-docker-flow:master-dev"
        )
        flow = Flow(
            "vjftw/invoke-docker-flow",
            "tool"
        )
        self.assertEqual(
            flow.get_development_container_name(),
            "vjftw/invoke-docker-flow:tool-master-dev"
        )

    def test_get_build_container_name(self):
        """
        Flow: Should return the build container name
        """
        flow = Flow(
            "vjftw/invoke-docker-flow"
        )
        self.assertEqual(
            flow.get_build_container_name(),
            "vjftw/invoke-docker-flow:master-1.0.0"
        )

        flow = Flow(
            "vjftw/invoke-docker-flow",
            "tool"
        )
        self.assertEqual(
            flow.get_build_container_name(),
            "vjftw/invoke-docker-flow:tool-master-1.0.0"
        )

    def test_get_build_container_tag(self):
        """
        Flow: Should return the build container tag
        """
        flow = Flow(
            "vjftw/invoke-docker-flow"
        )
        self.assertEqual(
            flow.get_build_container_tag(),
            "master-1.0.0"
        )

        flow = Flow(
            "vjftw/invoke-docker-flow",
            "tool"
        )
        self.assertEqual(
            flow.get_build_container_tag(),
            "tool-master-1.0.0"
        )

    def test_get_branch_container_name(self):
        """
        Flow: Should return the branch container name
        """
        flow = Flow(
            "vjftw/invoke-docker-flow"
        )
        self.assertEqual(
            flow.get_branch_container_name(),
            "vjftw/invoke-docker-flow:master"
        )

        flow = Flow(
            "vjftw/invoke-docker-flow",
            "tool"
        )
        self.assertEqual(
            flow.get_branch_container_name(),
            "vjftw/invoke-docker-flow:tool-master"
        )

    def test_get_branch_container_tag(self):
        """
        Flow: Should return the branch container tag
        """
        flow = Flow(
            "vjftw/invoke-docker-flow"
        )
        self.assertEqual(
            flow.get_branch_container_tag(),
            "master"
        )

        flow = Flow(
            "vjftw/invoke-docker-flow",
            "tool"
        )
        self.assertEqual(
            flow.get_branch_container_tag(),
            "tool-master"
        )
