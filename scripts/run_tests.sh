#!/bin/bash

nosetests --rednose --force-color --with-coverage --cover-html --cover-html-dir=coverage --all-modules --cover-package=invoke_tools tests/ -v
