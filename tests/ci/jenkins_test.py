"""
tests.invoke_tools.ci.jenkins_test
"""

import unittest
import mock
import json

from invoke_tools import ci


class JenkinsTests(unittest.TestCase):
    """
    Tests for Jenkins
    """

    def test_init(self):
        """
        invoke_tools.ci.jenkins.init: Should initialise the Jenkins object
        """
        jenkins = ci.Jenkins("https://jenkins.example.org", "job-name")
        self.assertIsInstance(jenkins, ci.Jenkins)

        git = mock.Mock()
        jenkins = ci.Jenkins("https://jenkins.example.org", "job-name", git)
        self.assertIsInstance(jenkins, ci.Jenkins)

    def test_get_last_successful_build_for_multi_branch(self):
        """
        invoke_tools.ci.jenkins.get_last_successful_build_sha: Should return the last successful build for a multi branch project
        """
        git = mock.Mock()
        git.get_branch = mock.Mock(return_value="develop")
        jenkins = ci.Jenkins("https://jenkins.example.org", "job-name", git)

        def requests_get(url):
            if url == "https://jenkins.example.org/job/job-name/job/develop/api/json?tree=lastSuccessfulBuild[number,url,timestamp]":
                json_file = "tests/json/ci-jenkins-multi-branch.json"
            elif url == "https://jenkins.example.org/job/job-name/job/develop/18/api/json?tree=actions[*[revision[SHA1]]]":
                json_file = "tests/json/ci-jenkins-multi-branch-build.json"
            else:
                raise ValueError("Invalid url: {0}".format(url))

            json_mock = mock.Mock()
            with open(json_file) as file:
                file_dict = json.loads(file.read())
            json_mock.json = mock.Mock(return_value=file_dict)
            return json_mock

        with mock.patch("invoke_tools.ci.jenkins.requests.get", side_effect=requests_get):
            self.assertEqual(
                jenkins.get_last_successful_build_sha(),
                "fd48c805a7684a5d268d0df4849c4cce3be6ce2f"
            )

    def test_get_last_successful_build_for_single_branch(self):
        """
        invoke_tools.ci.jenkins.get_last_successful_build_sha: Should return the last successful build for a single branch project
        """
        jenkins = ci.Jenkins("https://jenkins.example.org", "job-name")

        def requests_get(url):
            if url == "https://jenkins.example.org/job/job-name/api/json?tree=lastSuccessfulBuild[number,url,timestamp]":
                json_file = "tests/json/ci-jenkins-single-branch.json"
            elif url == "https://jenkins.example.org/job/job-name/62/api/json?tree=actions[*[revision[SHA1]]]":
                json_file = "tests/json/ci-jenkins-single-branch-build.json"
            else:
                raise ValueError("Invalid url: {0}".format(url))

            json_mock = mock.Mock()
            with open(json_file) as file:
                file_dict = json.loads(file.read())
            json_mock.json = mock.Mock(return_value=file_dict)
            return json_mock

        with mock.patch("invoke_tools.ci.jenkins.requests.get", side_effect=requests_get):
            self.assertEqual(
                jenkins.get_last_successful_build_sha(),
                "1b5cdf46844d011596b9b6a34c105b9a26c26a19"
            )

