""" Bot voor slack """
from datetime import datetime, date, timedelta
import os
import sys

from imap_tools import MailBox, AND
from pytz import timezone
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

EXAMPLE_COMMAND = 'help'

# instantiate Slack
app = App(
    token=os.environ.get('SLACK_BOT_TOKEN')
)

def message_help(extra):
  """ actie bij message: help """
  if len(extra) > 0:
    response = ' '.join(extra)
  else:
    response = "Dit zijn de opdrachten die deze bot kent\n" + \
               "• *help*: deze informatie\n" + \
               "* *datum <datum>*: aantal dagen vanaf <datum>\n" + \
               "* *datum <datum> <datum>*: aantal dagen tussen beide datums\n" + \
               "* *datum <datum> <aantal>*: datum <aantal> dagen na <datum>\n" + \
               "* *mail <naam>*: ongelezen berichten van deze mailbox\n" + \
               "* *mail alles*: aantal ongelezen berichten van alle bekende mailboxen\n" + \
               "\n" + \
               ""
  return response


def get_datum(tekst):
  """ mwak datum van tekst in juiste formaat """
  return datetime.strptime(tekst, '%Y-%m-%d').date()


def message_datum(extra):
  """ actie bij message: datum """
  if len(extra) == 0:
    return f'Vandaag is het {date.today()}'
  try:
    inputdatum = get_datum(extra[0])
  except ValueError as datumerror:
    fouttekst = datumerror
    return f'Gebruik: datum jjjj-mm-dd [jjjj-mm-dd|nnnnn]\n\nError: {fouttekst}'
  vandaag = date.today()
  verschil = (vandaag - inputdatum).days

  tweededatum = None
  tweedewaarde = None
  if len(extra) > 1:
    try:
      tweededatum = get_datum(extra[1])
    except ValueError as datumerror:
      try:
        tweedewaarde = int(extra[1])
      except ValueError as getalerror:
        return f'Gebruik: datum jjjj-mm-dd [jjjj-mm-dd|nnnnn]\n\nError: {datumerror}\n{getalerror}'
  returntekst = f'{inputdatum} is {verschil} dagen geleden'
  if tweededatum is None and tweedewaarde is None:
    return returntekst
  if tweededatum is None:
    nieuwedatum = inputdatum + timedelta(tweedewaarde)
    return f'{returntekst}\n{tweedewaarde} dagen na {inputdatum} is {nieuwedatum}'
  tweedeverschil = (tweededatum - inputdatum).days
  return f'{returntekst}\n{tweededatum} is {tweedeverschil} dagen na {inputdatum}'


def message_mail(extra):
  """ actie bij message: mail """
  if len(extra) != 1:
    return 'Gebruik mail <prefix>'
  inputname = extra[0]
  if inputname == 'alles':
    return 'ToDo'
  prefix = inputname.upper()
  try:
    mailuser = os.environ[f'MAIL_USER_{prefix}']
    mailpass = os.environ[f'MAIL_PASS_{prefix}']
    mailhost = os.environ['MAIL_HOST']
  except KeyError as keyerrormessage:
    return f'Geen gegevens gevonden voor {inputname}\n{keyerrormessage}'
  returntekst = 'Deze ongelezen mails:\n'
  with MailBox(mailhost).login(mailuser, mailpass) as mailbox:
    ongelezenmail = False
    for msg in mailbox.fetch(AND(seen=False), mark_seen=False):
      received = datetime.strftime(msg.date.astimezone(timezone('Europe/Amsterdam'))
                                   , '%Y-%m-%d %H:%M:%S')
      returntekst = f'{returntekst} {received} {msg.from_} {msg.subject}'
      ongelezenmail = True
  if ongelezenmail:
    return returntekst
  return 'Geen ongelezen mail'

@app.message('')
def handle_message(message, say):
  """
    Receives commands directed at the bot and determines if they
    are valid commands. If so, then acts on the commands. If not,
    returns back what it needs for clarification.
  """
  if message['user'] != 'U4HFYBQMU': # peter
    return
  command = message['text']
  try:
    splitmessage = command.split(' ')
    firstword = splitmessage[0]
    message = splitmessage[1:]
    if firstword == EXAMPLE_COMMAND:
      response = message_help(message)
    elif firstword == 'datum':
      response = message_datum(message)
    elif firstword == 'mail':
      response = message_mail(message)
    else:
      response = 'other'
  except:  # pylint: disable=bare-except
    print(f'ERR: {sys.exc_info()}')
    response = f'Er is iets foutgegaan: {sys.exc_info()[0]}'

  say(response)

if __name__ == "__main__":
  SocketModeHandler(app, os.environ['SLACK_APP_TOKEN']).start()
