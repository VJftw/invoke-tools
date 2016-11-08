from invoke import task
from docker import Client
import os

from invoke_tools import lxc, vcs

cli = Client(base_url='unix://var/run/docker.sock', timeout=600)

git = vcs.Git()
git.print_all()


@task
def test(ctx):
    tag = "invoke-tools-dev"
    lxc.Docker.build(cli, "Dockerfiles/python-2.Dockerfile", "{0}:2".format(tag))
    lxc.Docker.build(cli, "Dockerfiles/python-3.Dockerfile", "{0}:3".format(tag))

    cmd = "nosetests " \
          "--rednose " \
          "--force-color " \
          "--with-coverage " \
          "--cover-html " \
          "--cover-html-dir=coverage " \
          "--all-modules " \
          "--cover-package=invoke_tools " \
          "tests/ " \
          "-v"

    lxc.Docker.run(
        cli,
        tag="{0}:2".format(tag),
        command=cmd,
        volumes=[
            "{0}:/app".format(os.getcwd())
        ],
        working_dir="/app"
    )

    lxc.Docker.run(
        cli,
        tag="{0}:3".format(tag),
        command=cmd,
        volumes=[
            "{0}:/app".format(os.getcwd())
        ],
        working_dir="/app"
    )

    if os.getenv("CI") and git.get_branch() == "master":
        __publish_coverage()

def __publish_coverage():
    print("Downloading AWS CLI")
    for line in cli.pull('garland/aws-cli-docker:latest', stream=True):
        pass

    lxc.Docker.run(
        cli,
        tag="garland/aws-cli-docker:latest",
        command='aws s3 cp coverage/. s3://vjpatel.me/projects/invoke-tools/coverage/ --recursive --cache-control max-age=120',
        volumes=[
             "{0}:/app".format(os.getcwd())
        ],
        working_dir="/app",
        environment={
               "AWS_ACCESS_KEY_ID": os.getenv("AWS_ACCESS_KEY_ID"),
               "AWS_SECRET_ACCESS_KEY": os.getenv("AWS_SECRET_ACCESS_KEY"),
               "AWS_DEFAULT_REGION": "eu-west-1"
        }
    )


@task
def build(ctx):
    if os.getenv("CI") and git.get_branch() != "master":
        return

    print("#")
    print("# Building source and wheel distribution")
    print("#")

    lxc.Docker.clean(cli, ["build", "dist", "*.egg-info"])

    lxc.Docker.build(cli, "Dockerfiles/python-3.Dockerfile", "invoke-tools-dev:3")

    cmd = "python3 setup.py sdist bdist_wheel"
    lxc.Docker.run(
        cli,
        tag="invoke-tools-dev:3",
        command=cmd,
        volumes=[
            "{0}:/app".format(os.getcwd())
        ],
        working_dir="/app"
    )

@task
def publish(ctx):
    if git.get_branch() == "master":
        print("#")
        print("# Uploading with Twine")
        print("#")

        cmd = "twine upload --username {0} --password {1} dist/*".format(
            os.getenv('PYPI_USERNAME'),
            os.getenv('PYPI_PASSWORD')
        )
        lxc.Docker.run(
            cli,
            tag="invoke-tools-dev:3",
            command=cmd,
            volumes=[
                "{0}:/app".format(os.getcwd())
            ],
            working_dir="/app"
        )