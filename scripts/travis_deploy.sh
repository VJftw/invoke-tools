#!/bin/bash

if [ "$TRAVIS_BRANCH" = "master" ] && [ "$TRAVIS_PULL_REQUEST" = "false" ]; then
    echo ""
    echo "==="
    echo "Deploying to PyPI"
    echo "==="
    echo ""

    echo ""
    echo "Building source and wheel distribution"
    echo ""
    python setup.py sdist bdist_wheel

    echo ""
    echo "Uploading with Twine"
    echo ""
    twine --username $PYPI_USERNAME --password $PYPI_PASSWORD upload dist/*
fi
