"""
"""
# coding=utf-8

from .utils import Utils


class Flow:
    """
    """

    def __init__(
            self,
            repository,
            prefix=None,
            branch=None,
            version=None):
        """
        """
        self.__repository = repository
        self.__prefix = prefix
        if branch:
            self.__branch = branch
        else:
            self.__branch = Utils.get_branch()

        if version:
            self.__version = version
        else:
            self.__version = Utils.get_version()

    def get_development_container_name(self):
        """
        """
        if self.__prefix:
            return "{0}:{1}-{2}-dev".format(
                self.__repository,
                self.__prefix,
                self.__branch)
        else:
            return "{0}:{1}-dev".format(
                self.__repository,
                self.__branch)

    def get_build_container_tag(self):
        """
        """
        if self.__prefix:
            return "{0}-{1}-{2}".format(
                self.__prefix,
                self.__branch,
                self.__version)
        else:
            return "{0}-{1}".format(
                self.__branch,
                self.__version)

    def get_build_container_name(self):
        """
        """
        return "{0}:{1}".format(
            self.__repository,
            self.__build_container_tag)

    def get_branch_container_tag(self):
        """
        """
        if self.__prefix:
            return "{0}-{1}".format(
                self.__prefix,
                self.__branch)
        else:
            return "{0}".format(self.__branch)

    def get_branch_container_name(self):
        """
        """
        return "{0}:{1}".format(
            self.__repository,
            self.__branch_container_tag)
