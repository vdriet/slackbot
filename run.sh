cd /home/peter/dev/slackbot
. ./setslackenv.sh
docker stop slackbot
docker rm -f slackbot
docker run \
	--detach \
	--restart always \
	--name slackbot \
	--env SLACK_ID_RASPBOT=${SLACK_ID_RASPBOT} \
	slackbot
