"""
invoke_tools.ci.jenkins
"""

import requests


class Jenkins:
    """
    Jenkins
    """

    def __init__(self, address, job_name, git_for_multi_branch=None):
        """
        """
        self.__address = address
        self.__job_name = job_name
        self.__git = git_for_multi_branch
        pass

    def get_last_successful_build_sha(self):
        """
        """
        if self.__git:
            url = "{0}/job/{1}/job/{2}/api/json".format(
                self.__address,
                self.__job_name,
                self.__git.get_branch()
            )
        else:
            url = "{0}/job/{1}/api/json".format(
                self.__address,
                self.__job_name
            )

        response = requests.get("{0}?tree=lastSuccessfulBuild[number,url,timestamp]".format(url)).json()

        last_successful_build = response['lastSuccessfulBuild']

        response = requests.get("{0}api/json?tree=actions[*[revision[SHA1]]]".format(last_successful_build['url'])).json()

        sha = None
        for action in response['actions']:
            if "buildsByBranchName" in action:
                for key in action['buildsByBranchName']:
                    if "refs" not in key and "remotes" not in key:
                        sha = action['buildsByBranchName'][key]['revision']['SHA1']
                        break
                if sha:
                    break

        print("\nJenkins | Last Successful Build: {0} @ {1}\n".format(last_successful_build['number'], sha))

        return sha
