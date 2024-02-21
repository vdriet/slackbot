cd /home/peter/dev/slackbot
docker stop slackbot
docker rm -f slackbot
docker run \
	--detach \
	--restart always \
	--name slackbot \
	--env-file env.list \
	slackbot
