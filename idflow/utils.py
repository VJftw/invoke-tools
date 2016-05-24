"""
"""
# coding=utf-8

import os
import platform
from subprocess import check_output, CalledProcessError
import cpuinfo
import psutil

class Utils:
    """
    """

    @staticmethod
    def get_branch():
        """
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
        """
        try:
            return check_output(
                "git describe --tags".split(" ")
                ).decode('utf-8').strip()
        except CalledProcessError:
            return check_output(
                "git rev-parse --short HEAD".split(" ")
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
        print("  Kernel   :\t{0} {1}".format(kernel_info.release, kernel_info.version))
        print("  CPU Usage:\t{0}%".format(psutil.cpu_percent()))
        memory_info = psutil.virtual_memory()
        print("  RAM Usage:\t{0}% of {1:.2f} GB".format(memory_info.percent, memory_info.total / 1024 / 1024 / 1024))
        print("-------------------------------------------")
        print()
