from invoke import task
from docker import Client
from idflow import Utils, Docker
import os


cli = Client(base_url='unix://var/run/docker.sock', timeout=600)

@task
def test(ctx):
    tag="idflow-dev"
    Docker.build(cli, "Dockerfile.dev", tag)

    cmd = "nosetests --rednose --force-color --with-coverage --cover-html --cover-html-dir=coverage --all-modules --cover-package=idflow tests/ -v"

    Docker.run(
        cli,
        tag=tag,
        command=cmd,
        volumes=[
            "{0}:/app".format(os.getcwd())
            ],
        working_dir="/app"
    )

@task
def publish(ctx):
    if Utils.get_branch() == "master":
        print("#")
        print("# Building source and wheel distribution")
        print("#")

        Docker.clean(cli, ["build", "dist", "*.egg-info"])

        tag="idflow-dev"
        Docker.build(cli, "Dockerfile.dev", tag)

        cmd = "python3 setup.py sdist bdist_wheel"
        Docker.run(
            cli,
            tag=tag,
            command=cmd,
            volumes=[
                "{0}:/app".format(os.getcwd())
                ],
            working_dir="/app"
        )

        print("#")
        print("# Uploading with Twine")
        print("#")

        cmd = "twine upload --username {0} --password {1} dist/*".format(
            os.getenv('PYPI_USERNAME'),
            os.getenv('PYPI_PASSWORD')
        )
        Docker.run(
            cli,
            tag=tag,
            command=cmd,
            volumes=[
                "{0}:/app".format(os.getcwd())
                ],
            working_dir="/app"
        )

def __run(
    cli,
    tag,
    command,
    volumes=[],
    working_dir="",
    environment={}):
    """
    """
    print("#")
    print("# Running on {1}: {0}".format(command, tag))
    print("#")

    params = dict()
    params['image'] = tag
    params['command'] = command

    if len(volumes) > 0:
        params['volumes'] = volumes
        params['host_config'] = cli.create_host_config(binds=volumes)

    if working_dir != "":
        params['working_dir'] = working_dir
    if environment:
        params['environment'] = environment

    container = cli.create_container(**params)

    cli.start(container.get('Id'))
    for line in cli.attach(container=container.get('Id'), stream=True, logs=True):
        line = line.decode('utf-8')
        print(line, end="", flush=True)

    exit_code = cli.wait(container=container.get('Id'))
    if exit_code != 0:
        raise Exception("Exit Code: {0}".format(exit_code))
