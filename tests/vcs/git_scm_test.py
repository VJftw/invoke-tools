"""
tests.invoke_tools.vcs.git_scm_test
"""

import unittest
import mock

from invoke_tools import vcs


class GitTests(unittest.TestCase):
    """
    Tests for Git
    """

    def __se_repo_init(self, search_parent_directories=False):
        assert search_parent_directories, True
        self.repo = mock.Mock()
        self.repo.active_branch = "develop"
        self.repo.head.is_detached = False
        commit = mock.Mock()
        commit.__str__ = "abcdef12345sha"
        self.repo.commit = commit
        self.repo.tags = []

        self.repo.rev_parse = mock.Mock(return_value=self.repo.commit())

        return self.repo

    def test_init(self):
        """
        invoke_tools.vcs.git_scm.init: Should initialise the Git object
        """
        with mock.patch('invoke_tools.vcs.git_scm.Repo',
                        side_effect=self.__se_repo_init):
            git = vcs.Git()
            self.assertIsInstance(git, vcs.Git)

    def test_get_branch(self):
        """
        invoke_tools.vcs.git_scm.get_branch: Should return the current branch from the Git repository
        """
        with mock.patch('invoke_tools.vcs.git_scm.Repo',
                        side_effect=self.__se_repo_init):
            git = vcs.Git()
            self.assertEqual(git.get_branch(), "develop")

    def test_get_branch_detached(self):
        """
        invoke_tools.vcs.git_scm.get_branch: Should return the HEAD if the current revision is detached
        """
        def __se_repo(search_parent_directories=False):
            repo = self.__se_repo_init(search_parent_directories)
            repo.head.is_detached = True
            return repo

        with mock.patch('invoke_tools.vcs.git_scm.Repo',
                        side_effect=__se_repo):
            git = vcs.Git()
            self.assertEqual(git.get_branch(), "HEAD")

    def test_get_travis_branch(self):
        """
        invoke_tools.vcs.git_scm.get_branch: Should return the current branch on Travis
        """
        def se_os_getenv(var):
            if var == 'GIT_BRANCH':
                return 'travis'
            return None

        def __se_repo(search_parent_directories=False):
            repo = self.__se_repo_init(search_parent_directories)
            repo.head.is_detached = True
            return repo

        with mock.patch('invoke_tools.vcs.git_scm.Repo',
                        side_effect=__se_repo):
            git = vcs.Git()
            with mock.patch('idflow.utils.os.getenv',
                            side_effect=se_os_getenv):
                self.assertEqual(
                    git.get_branch(),
                    "travis"
                )

    def test_get_jenkins2_branch(self):
        """
        invoke_tools.vcs.git_scm.get_branch: Should return the current branch on Jenkins 2
        """
        def se_os_getenv(var):
            if var == 'BRANCH_NAME':
                return 'jenkins2'
            return None

        def __se_repo(search_parent_directories=False):
            repo = self.__se_repo_init(search_parent_directories)
            repo.head.is_detached = True
            return repo

        with mock.patch('invoke_tools.vcs.git_scm.Repo',
                        side_effect=__se_repo):
            git = vcs.Git()
            with mock.patch('idflow.utils.os.getenv',
                            side_effect=se_os_getenv):
                self.assertEqual(
                    git.get_branch(),
                    "jenkins2"
                )

    def test_get_version_with_tags(self):
        """
        invoke_tools.vcs.git_scm.get_version: Should return the current version tags if set
        """
        tag1 = mock.Mock()
        tag2 = mock.Mock()

        def __se_repo(search_parent_directories=False):
            repo = self.__se_repo_init(search_parent_directories)

            tag1.commit = "asdasda"
            tag2.commit = repo.commit()
            repo.tags = [
                tag1,
                tag2
            ]
            return repo

        with mock.patch('invoke_tools.vcs.git_scm.Repo',
                        side_effect=__se_repo):
            git = vcs.Git()
            self.assertEqual(git.get_version(), tag2)

    def test_get_version(self):
        """
        invoke_tools.vcs.git_scm.get_version: Should return the current version
        """
        with mock.patch('invoke_tools.vcs.git_scm.Repo',
                        side_effect=self.__se_repo_init):
            git = vcs.Git()
            self.assertEqual(git.get_version(), self.repo.commit())

    def test_get_changed_files(self):
        """
        invoke_tools.vcs.git_scm.get_changed_files: Should return an array of all the changed files
        """
        def __se_commit(sha=None):
            second_commit = mock.Mock()
            if sha == "first_commit":
                first_commit = mock.Mock()
                diff1 = mock.Mock()
                diff1.a_path = "this/is/a/path"
                diff2 = mock.Mock()
                diff2.a_path = "this/is/also/a/path"
                diff3 = mock.Mock()
                diff3.a_path = "this/is/another/path"

                first_commit.diff = mock.Mock(return_value=[
                    diff1, diff2, diff3
                ])
                return first_commit
            elif sha == "second_commit":
                return second_commit

        def __se_repo(search_parent_directories=False):
            repo = self.__se_repo_init(search_parent_directories)
            repo.commit = mock.Mock(side_effect=__se_commit)
            return repo

        with mock.patch('invoke_tools.vcs.git_scm.Repo',
                        side_effect=__se_repo):
            git = vcs.Git()

            self.assertEqual(git.get_changed_files("first_commit", "second_commit"), [
                "this/is/a/path",
                "this/is/also/a/path",
                "this/is/another/path"
            ])

    def test_get_changed_files_with_exclusions(self):
        """
        invoke_tools.vcs.git_scm.get_changed_files: Should return an array of all the changed files without exclusions
        """
        def __se_commit(sha=None):
            second_commit = mock.Mock()
            if sha == "first_commit":
                first_commit = mock.Mock()
                diff1 = mock.Mock()
                diff1.a_path = "this/is/a/path"
                diff2 = mock.Mock()
                diff2.a_path = "this/is/also/a/path"
                diff3 = mock.Mock()
                diff3.a_path = "this/is/another/path"

                first_commit.diff = mock.Mock(return_value=[
                    diff1, diff2, diff3
                ])
                return first_commit
            elif sha == "second_commit":
                return second_commit

        def __se_repo(search_parent_directories=False):
            repo = self.__se_repo_init(search_parent_directories)
            repo.commit = mock.Mock(side_effect=__se_commit)
            return repo

        with mock.patch('invoke_tools.vcs.git_scm.Repo',
                        side_effect=__se_repo):
            git = vcs.Git()

            self.assertEqual(git.get_changed_files("first_commit", "second_commit", ["this/is/another"]), [
                "this/is/a/path",
                "this/is/also/a/path"
            ])

