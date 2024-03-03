""" Bot voor slack """
from datetime import datetime
import os
import sys
from slack_sdk.rtm_v2 import RTMClient

BOT_ID = 'U4QCBT18A'
AT_BOT = f'<@{BOT_ID}>'
EXAMPLE_COMMAND = 'help'

# instantiate Slack
slack_id = os.environ['SLACK_ID_RASPBOT']
rtm = RTMClient(token=slack_id)

def message_help(extra):
  """ actie bij message help """
  if len(extra) > 0:
    print('join')
    response = ' '.join(extra)
  else:
    print('default')
    response = "Dit zijn de opdrachten die deze bot kent\n" + \
      "• *help*: deze informatie\n" + \
      ""
  return response


def message_datum(extra):
  """ actie bij message datum """
  try:
    inputdatum = datetime.strptime(extra, '%d-%m-%Y')
  except ValueError:
    return 'Gebruik: datum dd-mm-jjjj'
  vandaag = datetime.now()
  verschil = (vandaag - inputdatum).days
  return f'{extra} is {verschil} dagen geleden'


@rtm.on("message")
def handle(client: RTMClient, event: dict):
  """
    Receives commands directed at the bot and determines if they
    are valid commands. If so, then acts on the commands. If not,
    returns back what it needs for clarification.
  """
  web_client = client.web_client
  command = event['text']
  channel_id = event['channel']
  thread_ts = event['ts']
  if event['user'] != 'U4HFYBQMU':
    return
  try:
    splitmessage = command.split(' ')
    firstword = splitmessage[0]
    message = splitmessage[1:]
    if firstword == EXAMPLE_COMMAND:
      print(message)
      response = message_help(message)
    elif firstword == 'datum' :
      response = message_datum(message)
    else :
      response = 'other'
  except: # pylint: disable=bare-except
    print(f'ERR: {sys.exc_info()}')
    response = f'Er is iets foutgegaan: {sys.exc_info()[0]}'

  web_client.chat_postMessage(
    channel=channel_id,
    text=response,
    thread_ts=thread_ts
  )

if __name__ == "__main__":
  rtm.start()
