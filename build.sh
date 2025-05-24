#!/bin/bash
set -e
pip install -q -r requirements.txt
pip list --outdated
pylint *.py
coverage run -m pytest
coverage report -m
uname -n | grep -v penguin && docker build --tag slackbot .
