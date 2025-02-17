#!/bin/bash
set -e
pip install -q -r requirements.txt
pip list --outdated
pylint *.py
coverage run -m pytest
coverage report -m
docker build --tag slackbot .
