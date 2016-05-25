"""
Utils tests
"""
# coding=utf-8

import unittest
import mock
from subprocess import CalledProcessError

from idflow import Utils


class UtilsTest(unittest.TestCase):
    """
    Tests for Utils
    """

    def test_get_travis_branch(self):
        """
        Utils: Should return the branch on Travis
        """
        def se_os_getenv(var):
            if var == 'GIT_BRANCH':
                return 'travis'
            return None

        with mock.patch('idflow.utils.os.getenv',
                        side_effect=se_os_getenv):
            self.assertEqual(
                Utils.get_branch(),
                "travis"
            )

    def test_get_jenkins2_branch(self):
        """
        Utils: Should return the branch on Jenkins 2
        """
        def se_os_getenv(var):
            if var == 'BRANCH_NAME':
                return 'jenkins2'
            return None

        with mock.patch('idflow.utils.os.getenv',
                        side_effect=se_os_getenv):
            self.assertEqual(
                Utils.get_branch(),
                "jenkins2"
            )

    def test_get_git_branch(self):
        """
        Utils: Should return the branch using Git
        """
        def se_check_output(cmds):
            if cmds == "git rev-parse --abbrev-ref HEAD".split(" "):
                return "git-branch\n".encode('utf-8')
            raise CalledProcessError(1, cmds)

        with mock.patch('idflow.utils.os.getenv', return_value=None):
            with mock.patch('idflow.utils.check_output',
                            side_effect=se_check_output):
                self.assertEqual(
                    Utils.get_branch(),
                    "git-branch"
                )

    def test_get_version_with_tags(self):
        """
        Utils: Should return the version using tags
        """
        def se_check_output(cmds):
            if cmds == "git describe --tags".split(" "):
                return "tag-version\n".encode('utf-8')
            raise CalledProcessError(1, cmds)

        with mock.patch('idflow.utils.check_output',
                        side_effect=se_check_output):
            self.assertEqual(
                Utils.get_version(),
                "tag-version"
            )

    def test_get_version_with_tags(self):
        """
        Utils: Should return the version using the short commit
        """
        def se_check_output(cmds):
            if cmds == "git rev-parse --short HEAD".split(" "):
                return "short-commit-version\n".encode('utf-8')
            raise CalledProcessError(1, cmds)

        with mock.patch('idflow.utils.check_output',
                        side_effect=se_check_output):
            self.assertEqual(
                Utils.get_version(),
                "short-commit-version"
            )
