import os
import sys
import time
import subprocess

from checkstatus import do_checks
from checkstatus import show_config
from checkstatus import add_host
from checkstatus import change_host
from checkstatus import rename_host
from checkstatus import remove_host
from slack_sdk.rtm_v2 import RTMClient
from waterstand import haalwaterstand_en_post

from google_trans_new import google_translator
BOT_ID = 'U4QCBT18A'
# constants
AT_BOT = '<@{}>'.format(BOT_ID)
EXAMPLE_COMMAND = 'help'

# instantiate Slack
slack_id = os.environ['SLACK_ID_RASPBOT']
rtm = RTMClient(token=slack_id)

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
    if command.startswith(EXAMPLE_COMMAND):
      response = "Dit zijn de opdrachten die deze bot kent\n" + \
        "• *help*: deze informatie\n" + \
        "• *waterstand*: forceert de waterstand melding naar <#C4HQXHGR3|waterstand>\n" + \
        "• *ssl*: toont ssl-status van een host\n" + \
        "• *check*: controleert de status van de geconfigureerde hosts\n" + \
        "• *check list*: toont de geconfigureerde hosts\n" + \
        "• *check add <name> <host> <port> <status> <url>*: voeg nieuwe check toe\n" + \
        "• *check change <name> <host> <port> <status> <url>*: wijzig de gegevens\n" + \
        "• *check rename <name> <newname>*: verander de naam van een check\n" + \
        "• *check remove <name>*: verwijder de gegevens\n" + \
        ""
    elif command.startswith("cmd"):
      cmd = command[4:]
      response = subprocess.check_output([cmd], shell=True).decode("utf-8")
    elif command.startswith("ssl"):
      words = command.split()
      if len(words) == 1:
        response = "ssl <host>"
      else:
        starthost = words[1].find('|') + 1
        endhost = words[1].find('>')
        host = words[1][starthost:endhost]
        cmd = "echo -n | openssl s_client -servername " + host + " -connect " + \
              host + ":443 2>/dev/null | openssl x509 -noout -dates -issuer -subject"
        response = '```' + subprocess.check_output([cmd], shell=True).decode("utf-8") + '```'
    elif command.startswith("waterstand"):
      response = "kijk in <#C4HQXHGR3|waterstand> daar komt de output"
      haalwaterstand_en_post()
    elif command.startswith("check"):
      words = command.split()
      if len(words) == 1:
        response = do_checks()
      elif words[1] == 'list':
        response = show_config()
      elif words[1] == 'change' or words[1] == 'add':
        aantalparam = len(words)

        if aantalparam != 6 and aantalparam != 7:
          response = 'Verkeerde syntax'
        else:
          starthost = words[3].find('|') + 1
          endhost = words[3].find('>')
          host = words[3][starthost:endhost]

          if aantalparam == 6:
            location = None
          else:
            startloc = words[6].find('<') + 1
            endloc = words[6].find('>')
            location = words[6][startloc:endloc]
          if words[1] == 'change':
            response = change_host(words[2], host, words[4], int(words[5]), location)
          else:
            response = add_host(words[2], host, words[4], int(words[5]), location)
      elif words[1] == 'rename':
        if len(words) != 4:
          response = 'Verkeerde syntax'
        else:
          response = rename_host(words[2], words[3])
      elif words[1] == 'remove':
        if len(words) != 3:
          response = 'Verkeerde syntax'
        else:
          response = remove_host(words[2])
    else:
      for f in event['files'] :
        ftype = f['filetype']
        text = f['preview']
        #print(f'{ftype} met tekst:{text}')
        tl = google_translator()
        trans = tl.translate(text, lang_src ='en', lang_tgt='nl')
        #print(trans)
        response = f'vertaling: [{trans}]'
  except:
    print('ERR: {}'.config(sys.exc_info()))
    response = 'Er is iets foutgegaan: {}'.format(sys.exc_info()[0])

  web_client.chat_postMessage(
      channel=channel_id,
      text=response,
      thread_ts=thread_ts
    )
  slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)

if __name__ == "__main__":
  rtm.start()
