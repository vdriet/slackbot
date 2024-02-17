docker stop slackbot
docker rm -f slackbot
docker run --detach --restart always --name slackbot slackbot
