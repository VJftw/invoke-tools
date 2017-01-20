"""
invoke_tools.lxc.docker
"""
from __future__ import print_function
import os
import json
import getpass


class Docker:
    """
    Docker
    """

    @staticmethod
    def __print_line(line):
        """
        """
        try:
            line = line.decode('utf-8')
        except:
            print("Could not decode line")
            return
        try:
            line = json.loads(line)

            if "stream" in line:
                line = line["stream"]
                pass
            elif "status" in line:
                if line["status"] == "Downloading" or line["status"] == "Extracting":
                    return
                o = line["status"]
                if "progress" in line:
                    o += " " + line["progress"]
                if "id" in line:
                    o = line["id"] + " " + o
                line = o
        except:
            pass

        print(line, end="", flush=True)

    @staticmethod
    def build(cli, dockerfile, tag):
        print("#")
        print("# Building Docker image from '{0}' with tag '{1}'".format(dockerfile, tag))
        print("#")
        for line in cli.build(
                dockerfile=dockerfile,
                pull=True,
                path=".",
                rm=True,
                tag=tag):
            Docker.__print_line(line)
        print()

    @staticmethod
    def execute(cli, container_id, cmd):
        print("#")
        print("# Executing on {1}: {0}".format(cmd, container_id))
        print("#")

        exec_container = cli.exec_create(
            container=container_id,
            cmd=cmd
            # user='root' if CI else 'app'
        )

        for line in cli.exec_start(
                exec_id=exec_container.get('Id'),
                stream=True):
            Docker.__print_line(line)
        print()

        inspect = cli.exec_inspect(exec_container.get('Id'))
        exit_code = inspect.get('ExitCode')
        if exit_code != 0:
            cli.stop(container_id)
            cli.remove_container(container_id)
            raise Exception("Exit Code: {0}\n{1}".format(exit_code, inspect))

    @staticmethod
    def clean(cli, objs):
        print("#")
        print("# Cleaning files & directories: {0}".format(objs))
        print("#")

        cli.pull("alpine:latest")
        container = cli.create_container(
            image='alpine:latest',
            volumes=[
                '{0}:/app'.format(os.getcwd())
            ],
            working_dir='/app',
            host_config=cli.create_host_config(binds=[
                '{0}:/app'.format(os.getcwd())
            ]),
            command='/bin/sh -c "rm -rf {0}"'.format(" ".join(objs))
        )
        response = cli.start(container=container.get('Id'))
        cli.wait(container=container.get('Id'), timeout=600)
        print(response)
        cli.remove_container(container.get('Id'))
        print()

    @staticmethod
    def push(cli, tags):
        """
        """
        for tag in tags:
            print("#")
            print("# Pushing {0} to Registry".format(tag))
            print("#")

            for line in cli.push(tag, stream=True):
                Docker.__print_line(line)
            print()

    @staticmethod
    def login(cli):
        """
        """
        if os.getenv('DOCKER_EMAIL') and os.getenv('DOCKER_USERNAME') and os.getenv('DOCKER_PASSWORD'):
            email = os.getenv('DOCKER_EMAIL')
            username = os.getenv('DOCKER_USERNAME')
            password = os.getenv('DOCKER_PASSWORD')
        else:
            email = input('Docker email:')
            username = input('Docker username:')
            password = getpass.getpass('Docker password:')

        cli.login(
            username=username,
            email=email,
            password=password,
            registry='https://index.docker.io/v1/'
        )
        print()

        return cli, username

    @staticmethod
    def run(
            cli,
            tag,
            command,
            volumes=None,
            working_dir="",
            environment=None,
            links=None,
            detach=False):
        """
        """
        if environment is None:
            environment = {}
        if volumes is None:
            volumes = []
        print("#")
        print("# Running on {1}: {0}".format(command, tag))
        print("#")

        params = dict()
        params['image'] = tag
        params['command'] = command

        if len(volumes) > 0:
            params['volumes'] = volumes
            params['host_config'] = cli.create_host_config(binds=volumes, links=links)

        if working_dir != "":
            params['working_dir'] = working_dir
        if environment:
            params['environment'] = environment

        if links:
            params['host_config'] = cli.create_host_config(binds=volumes, links=links)

        container = cli.create_container(**params)

        cli.start(container.get('Id'))
        if detach:
            return container

        for line in cli.attach(container=container.get('Id'), stream=True, logs=True):
            Docker.__print_line(line)

        exit_code = cli.wait(container=container.get('Id'))
        cli.remove_container(container.get('Id'))

        if exit_code != 0:
            raise Exception("Exit Code: {0}".format(exit_code))
