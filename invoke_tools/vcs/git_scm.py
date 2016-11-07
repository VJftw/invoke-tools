"""
invoke_tools.vcs.git_scm
"""
from git import Repo
import os


class Git:
    """
    Git
    """

    def __init__(self):
        """
        """
        self.repo = Repo(search_parent_directories=True)
        pass

    def get_branch(self):
        """
        :return:
        """
        if self.repo.head.is_detached:
            if os.getenv('GIT_BRANCH'):
                branch = os.getenv('GIT_BRANCH')
            elif os.getenv('BRANCH_NAME'):
                branch = os.getenv('BRANCH_NAME')
            else:
                branch = "HEAD"
        else:
            branch = str(self.repo.active_branch)

        return branch.replace("/", "_")

    def get_version(self):
        """
        :return:
        """
        tag = next((tag for tag in self.repo.tags if tag.commit == self.repo.commit()), None)
        if tag:
            return tag

        return self.repo.rev_parse(str(self.repo.commit()))

    def get_changed_files(self, first_sha, second_sha, exclude_paths=None):
        """
        :param first_sha:
        :param second_sha:
        :param exclude_paths:
        :return:
        """
        if not exclude_paths:
            exclude_paths = []

        first_commit = self.repo.commit(first_sha)
        second_commit = self.repo.commit(second_sha)

        diffs = first_commit.diff(second_commit)
        changed_files = []

        for diff in diffs:
            excluded = False
            for exclude in exclude_paths:
                if diff.a_path.startswith(exclude):
                    excluded = True

            if not excluded:
                changed_files.append(diff.a_path)

        return changed_files

    def print_all(self):
        """
        :return:
        """
        output = "\n\n# Git information  \n" \
                 "-------------------------------------------\n" \
                 "  Branch :\t{0}\n" \
                 "  Version:\t{1}\n" \
                 "  Summary:\t{2}\n" \
                 "-------------------------------------------\n\n".format(
            self.get_branch(),
            str(self.get_version()),
            self.repo.commit().summary,
        )

        print(output)
