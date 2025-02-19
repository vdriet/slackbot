""" testen voor de slackbot datumfuncties """
import pytest
from unittest.mock import patch

@pytest.fixture
def mock_environment(monkeypatch):
  monkeypatch.setenv("SLACK_APP_TOKEN", "DUMMY")
  monkeypatch.setenv("SLACK_BOT_TOKEN", "DUMMY")


@patch('slack_bolt.App')
def test_get_datum(mock_app, mock_environment):
  import slackbot
  from datetime import date

  invoer = '2024-12-01'
  verwachting = date(2024, 12, 1)
  resultaat = slackbot.get_datum(invoer)
  assert resultaat == verwachting


def test_message_datum_leeg(mock_environment):
  import slackbot

  invoer = ''
  verwachting = f'Vandaag is het'
  resultaat = slackbot.message_datum(invoer)
  assert resultaat[:len(verwachting)] == verwachting


def test_message_datum_fout(mock_environment):
  import slackbot

  invoer = ['01-12-2024']  # fout formaat
  verwachting = 'Gebruik: datum jjjj-mm-dd [jjjj-mm-dd|nnnnn]'
  resultaat = slackbot.message_datum(invoer)
  assert resultaat[:len(verwachting)] == verwachting


def test_message_datum_enkel(mock_environment):
  import slackbot

  invoer = ['2024-11-29']
  verwachtingbegin = '2024-11-29 is '
  verwachtingeinde = ' dagen geleden'
  resultaat = slackbot.message_datum(invoer)
  assert resultaat.startswith(verwachtingbegin)
  assert resultaat.endswith(verwachtingeinde)


def test_message_datum_dubbel(mock_environment):
  import slackbot

  invoer = ['2005-04-03', '2013-12-11']
  verwachtingbegin = f'{invoer[0]} is '
  verwachtingeinde = f'{invoer[1]} is 3174 dagen na {invoer[0]}'
  resultaat = slackbot.message_datum(invoer)
  assert resultaat.startswith(verwachtingbegin)
  assert resultaat.endswith(verwachtingeinde)


def test_message_datum_getal(mock_environment):
  import slackbot

  invoer = ['2005-04-03', '3174']
  verwachtingbegin = f'{invoer[0]} is '
  verwachtingeinde = f'{invoer[1]} dagen na {invoer[0]} is 2013-12-11'
  resultaat = slackbot.message_datum(invoer)
  assert resultaat.startswith(verwachtingbegin)
  assert resultaat.endswith(verwachtingeinde)


def test_message_datum_datum_noch_getal(mock_environment):
  import slackbot

  invoer = ['2005-04-03', 'abc']
  verwachting = "Gebruik: datum jjjj-mm-dd [jjjj-mm-dd|nnnnn]\n\n" + \
                "Error: time data 'abc' does not match format '%Y-%m-%d'\n" + \
                "invalid literal for int() with base 10: 'abc'"
  resultaat = slackbot.message_datum(invoer)
  assert resultaat == verwachting
