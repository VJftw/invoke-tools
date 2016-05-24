"""
"""
import os
import json


class Docker:

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
        except:
            print(line, end="", flush=True)
            return

        if "stream" in line:
            print(line["stream"], end="", flush=True)
        elif "status" in line:
            o = line["status"]
            if "progress" in line:
                o += " " + line["progress"]
            if "id" in line:
                o = line["id"] + " " + o
            print(o, end="", flush=True)

    @staticmethod
    def build(cli, dockerfile, tag):
        for line in cli.build(
            dockerfile=dockerfile,
            pull=True,
            path=".",
            rm=True,
            tag=tag
        ):
            Docker.__print_line(line)

    @staticmethod
    def execute(cli, container_id, cmd):
        print("Executing: {0}".format(cmd))
        execute = cli.exec_create(
            container=container_id,
            cmd=cmd,
            user='root' if CI else 'app'
        )

        for line in cli.exec_start(
            exec_id=execute.get('Id'),
            stream=True
        ):
            Docker.__print_line(line)

        inspect = cli.exec_inspect(execute.get('Id'))
        exit_code = inspect.get('ExitCode')
        if exit_code != 0:
            cli.stop(container_id)
            cli.remove_container(container_id)
            raise Exception("Exit Code: {0}\n{1}".format(exit_code, inspect))

    @staticmethod
    def clean(cli, objs):
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
        print('/bin/sh -c "rm -rf {0}"'.format(" ".join(objs)))
        response = cli.start(container=container.get('Id'))
        cli.wait(container=container.get('Id'), timeout=600)
        print(response)
        cli.remove_container(container.get('Id'))

    @staticmethod
    def push(cli, tags):
        """
        """
        for tag in tags:
            print("# Pushing {0} to Registry".format(tag))
            for line in cli.push(tag, stream=True):
                Docker.__print_line(line)
