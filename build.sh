#!/bin/bash
set -e
pip install -r requirements.txt
pip list --outdated
pylint slackbot/*.py
pytest
docker build --tag slackbot .
