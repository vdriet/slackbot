#!/bin/sh
# run.sh
# navigate to home directory, then to this directory, then execute python script, then back home

sleep 10

cd /home/peter/dev/slackbot
. /home/peter/dev/slackbot/env.sh
. /home/peter/dev/slackbot/setenv.sh
python3 . > /home/peter/logs/slackbot.log 2>&1
cd /
