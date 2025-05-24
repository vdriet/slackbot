""" Bot voor slack """
import os
import sys
from datetime import datetime, date, timedelta

from imap_tools import MailBox, AND
from pytz import timezone
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

EXAMPLE_COMMAND = 'help'

# instantiate Slack
app = App(
  token=os.environ.get('SLACK_BOT_TOKEN')
)


def message_help(extra: list[str]) -> str:
  """
  Provides help information regarding the commands available in the bot. If
  additional arguments are provided, they are joined into a response string;
  otherwise, a default help message is returned.

  Args:
      extra (list[str]): A list of additional strings to include in the response.

  Returns:
      str: A help message detailing the commands supported by the bot, or a
      custom message based on the extra arguments provided.
  """
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


def get_datum(tekst: str) -> date:
  """
  Parses a given string and converts it into a date object.

  This function takes a string representing a date in the format '%Y-%m-%d' and
  returns a corresponding date object. It is used for converting textual date
  representations into Python date objects for further usage or manipulation.

  Args:
      tekst (str): The string containing the date in the format '%Y-%m-%d'.

  Returns:
      date: The corresponding date object parsed from the input string.

  Raises:
      ValueError: If the input string does not match the expected date format.
  """
  return datetime.strptime(tekst, '%Y-%m-%d').date()


def message_datum(extra: list[str]) -> str:
  """
  Generates a message about dates and their differences. It calculates the number
  of days between a given input date and today, with optional functionality for
  calculating differences with a second date or adding a number of days to the
  input date.

  Parameters:
  extra (list): A list of strings where the first element is a date in the
                format 'jjjj-mm-dd', and the optional second element is either
                a date in the same format or a number.

  Returns:
  str: A formatted string providing information about the input date, the
       difference in days between the dates, or the resulting date after adding
       a number of days to the input date.

  Raises:
  ValueError: If an input date does not match the 'jjjj-mm-dd' format or if an
              error occurs while converting a string to an integer.
  """
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


def leesmail(mailhost: str, mailuser: str, mailpass: str) -> str:
  """
  Fetch and list unread emails from a mailbox without marking them as read.

  Args:
      mailhost (str): The mail server hostname or address to connect to.
      mailuser (str): The username or email address of the mailbox to log in to.
      mailpass (str): The password for the corresponding mailbox user.

  Returns:
      str: A string summarizing the unread emails, including their date, sender,
      and subject. If no unread emails are present, a default message indicating
      no new mail is returned.
  """
  with MailBox(mailhost).login(mailuser, mailpass) as mailbox:
    returntekst = 'Deze ongelezen mails:\n'
    ongelezenmail = False
    for msg in mailbox.fetch(AND(seen=False), mark_seen=False):
      received = datetime.strftime(msg.date.astimezone(timezone('Europe/Amsterdam'))
                                   , '%Y-%m-%d %H:%M:%S')
      returntekst = f'{returntekst} {received} {msg.from_} {msg.subject}'
      ongelezenmail = True
  if ongelezenmail:
    return returntekst
  return 'Geen ongelezen mail'


def message_mail(extra: list[str]) -> str:
  """
  Generates and handles an email message based on the specified prefix provided in the argument
  list.

  This function expects a single argument, `extra`, which is a list containing one email prefix.
  Using the prefix, it attempts to retrieve the corresponding email credentials from the
  environment variables and processes the email.

  Arguments:
      extra (list of str): A list containing one element, the email prefix, or the keyword 'alles'.

  Returns:
      str: A result message indicating the outcome of the operation, or an error message in case
           of failure.
  """
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
  return leesmail(mailhost, mailuser, mailpass)


@app.message('')
def handle_message(message: dict, say) -> None:
  """
  Handles Slack messages and responds based on specific commands.

  This function listens for incoming Slack messages and processes them if
  the message's user is 'U4HFYBQMU' (identified as 'peter'). It checks the
  command in the message text and delegates the message to appropriate
  handlers or provides a fallback response.

  Parameters:
  message : dict
      The Slack message payload that includes details such as the user and
      message text.
  say : Callable
      A callable function to send a response message back to the Slack channel.

  Raises:
  Exception
      Any unhandled exceptions during message handling. The function catches
      these to avoid interrupting execution and logs them for debugging.
  """
  if message['user'] != 'U4HFYBQMU':  # peter
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
