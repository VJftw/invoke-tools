"""
idflow.Utils
"""
# coding=utf-8

import os
import platform
from subprocess import check_output, CalledProcessError
import cpuinfo
import psutil


class Utils:
    """
    Utils
    """

    @staticmethod
    def get_branch():
        """
        Returns the current code branch
        """
        if os.getenv('GIT_BRANCH'):
            # Travis
            branch = os.getenv('GIT_BRANCH')
        elif os.getenv('BRANCH_NAME'):
            # Jenkins 2
            branch = os.getenv('BRANCH_NAME')
        else:
            branch = check_output(
                "git rev-parse --abbrev-ref HEAD".split(" ")
                ).decode('utf-8').strip()

        return branch.replace("/", "_")

    @staticmethod
    def get_version():
        """
        Returns the current code version
        """
        try:
            return check_output(
                "git describe --tags".split(" ")
                ).decode('utf-8').strip()
        except CalledProcessError:
            return check_output(
                "git rev-parse --short HEAD".split(" ")
                ).decode('utf-8').strip()

    def get_current_commit_sha():
        """
        Returns the current git commit
        """
        return check_output(
            "git rev-parse HEAD".split(" ")
            ).decode('utf-8').strip()

    def jenkins_last_build_sha():
        """
        Returns the sha of the last completed jenkins build for this project.
        Expects JOB_URL in environment
        """
        job_url = os.getenv('JOB_URL')
        job_json_url = "{0}/api/json".format(job_url)
        response = urllib.urlopen(job_json_url)
        job_data = json.loads(response.read())

        last_completed_build_url = job_data['lastCompletedBuild']['url']
        last_complete_build_json_url = "{0}/api/json".format(last_completed_build_url)

        response = urllib.urlopen(last_complete_build_json_url)
        last_completed_build = json.loads(response.read())

        return last_completed_build[1]['lastBuiltRevision']['SHA1'] # needs testing


    def get_changed_files_from(old_commit_sha, new_commit_sha):
        """
        Returns a list of the files changed between two commits
        """
        return check_output(
            "git diff-tree --no-commit-id --name-only -r {0}..{1}".format(
                old_commit_sha,
                new_commit_sha
            ).split(" ")
            ).decode('utf-8').strip()

    @staticmethod
    def print_system_info():
        """
        """
        info = cpuinfo.get_cpu_info()
        print()
        print("# System information  ")
        print("-------------------------------------------")
        print("  Hostname :\t{0}".format(platform.node()))
        print("  Processor:\t{0}".format(info['brand']))
        print("  System   :\t{0}".format(platform.system()))
        kernel_info = platform.uname()
        print("  Kernel   :\t{0} {1}".format(kernel_info.release,
                                             kernel_info.version))
        print("  CPU Usage:\t{0}%".format(psutil.cpu_percent()))
        memory_info = psutil.virtual_memory()
        print("  RAM Usage:\t{0}% of {1:.2f} GB".format(
            memory_info.percent, memory_info.total / 1073741824))
        print("-------------------------------------------")
        print()
