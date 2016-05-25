"""
Flow tests
"""
# coding=utf-8

import unittest
import mock
import os

# import sys
#
# utils_mock = mock.Mock()
# utils_mock.Utils.get_branch.return_value = "master"
# utils_mock.Utils.get_version.return_value = "1.0.0"
# sys.modules['idflow.utils'] = utils_mock

from idflow import Flow


class FlowTests(unittest.TestCase):
    """
    Tests for Flow
    """

    def setUp(self):
        self.os_environ = os.environ.copy()

    def tearDown(self):
        os.environ = self.os_environ

    def __se_check_output(self, cmds):
        if cmds == "git describe --tags".split(" "):
            return "1.0.0".encode('utf-8')
        elif cmds == "git rev-parse --short HEAD".split(" "):
            return "fe5a7e3".encode('utf-8')
        elif cmds == "git rev-parse --abbrev-ref HEAD".split(" "):
            return "develop".encode('utf-8')

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
        with mock.patch('idflow.utils.check_output',
                        side_effect=self.__se_check_output):
            flow = Flow(
                "vjftw/invoke-docker-flow"
            )
            self.assertEqual(
                flow.get_development_container_name(),
                "vjftw/invoke-docker-flow:develop-dev"
            )
            flow = Flow(
                "vjftw/invoke-docker-flow",
                "tool"
            )
            self.assertEqual(
                flow.get_development_container_name(),
                "vjftw/invoke-docker-flow:tool-develop-dev"
            )

    def test_get_build_container_name(self):
        """
        Flow: Should return the build container name
        """
        with mock.patch('idflow.utils.check_output',
                        side_effect=self.__se_check_output):
            flow = Flow(
                "vjftw/invoke-docker-flow"
            )
            self.assertEqual(
                flow.get_build_container_name(),
                "vjftw/invoke-docker-flow:develop-1.0.0"
            )

            flow = Flow(
                "vjftw/invoke-docker-flow",
                "tool"
            )
            self.assertEqual(
                flow.get_build_container_name(),
                "vjftw/invoke-docker-flow:tool-develop-1.0.0"
            )

    def test_get_build_container_tag(self):
        """
        Flow: Should return the build container tag
        """
        with mock.patch('idflow.utils.check_output',
                        side_effect=self.__se_check_output):
            flow = Flow(
                "vjftw/invoke-docker-flow"
            )
            self.assertEqual(
                flow.get_build_container_tag(),
                "develop-1.0.0"
            )

            flow = Flow(
                "vjftw/invoke-docker-flow",
                "tool"
            )
            self.assertEqual(
                flow.get_build_container_tag(),
                "tool-develop-1.0.0"
            )

    def test_get_branch_container_name(self):
        """
        Flow: Should return the branch container name
        """
        with mock.patch('idflow.utils.check_output',
                        side_effect=self.__se_check_output):
            flow = Flow(
                "vjftw/invoke-docker-flow"
            )
            self.assertEqual(
                flow.get_branch_container_name(),
                "vjftw/invoke-docker-flow:develop"
            )

            flow = Flow(
                "vjftw/invoke-docker-flow",
                "tool"
            )
            self.assertEqual(
                flow.get_branch_container_name(),
                "vjftw/invoke-docker-flow:tool-develop"
            )

    def test_get_branch_container_tag(self):
        """
        Flow: Should return the branch container tag
        """
        with mock.patch('idflow.utils.check_output',
                        side_effect=self.__se_check_output):
            flow = Flow(
                "vjftw/invoke-docker-flow"
            )
            self.assertEqual(
                flow.get_branch_container_tag(),
                "develop"
            )

            flow = Flow(
                "vjftw/invoke-docker-flow",
                "tool"
            )
            self.assertEqual(
                flow.get_branch_container_tag(),
                "tool-develop"
            )
