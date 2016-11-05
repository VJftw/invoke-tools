from invoke import task
from docker import Client
from idflow import Utils, Docker
import os

cli = Client(base_url='unix://var/run/docker.sock', timeout=600)


@task
def test(ctx):
    tag = "idflow-dev"
    Docker.build(cli, "Dockerfile.dev", tag)

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
def publish_coverage(ctx):
    if Utils.get_branch() == "master":
        Docker.run(
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
def publish(ctx):
    if Utils.get_branch() == "master":
        print("#")
        print("# Building source and wheel distribution")
        print("#")

        Docker.clean(cli, ["build", "dist", "*.egg-info"])

        tag = "idflow-dev"
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
