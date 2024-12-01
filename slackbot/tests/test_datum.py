""" testen voor de slackbot datumfuncties """
import pytest

@pytest.fixture
def mock_env_slack_id(monkeypatch):
  monkeypatch.setenv("SLACK_ID_RASPBOT", "DUMMY")

def test_get_datum(mock_env_slack_id):
  from slackbot import slackbot
  from datetime import date

  invoer = '2024-12-01'
  verwachting = date(2024, 12, 1)
  resultaat = slackbot.get_datum(invoer)
  assert resultaat == verwachting

def test_message_datum_leeg(mock_env_slack_id):
  from slackbot import slackbot

  invoer = ''
  verwachting = f'Vandaag is het'
  resultaat = slackbot.message_datum(invoer)
  assert resultaat[:len(verwachting)] == verwachting

def test_message_datum_fout(mock_env_slack_id):
  from slackbot import slackbot

  invoer = ['01-12-2024'] # fout formaat
  verwachting = 'Gebruik: datum jjjj-mm-dd [jjjj-mm-dd|nnnnn]'
  resultaat = slackbot.message_datum(invoer)
  assert resultaat[:len(verwachting)] == verwachting

def test_message_datum_enkel(mock_env_slack_id):
  from slackbot import slackbot

  invoer = ['2024-11-29']
  verwachtingbegin = '2024-11-29 is '
  verwachtingeinde = ' dagen geleden'
  resultaat = slackbot.message_datum(invoer)
  assert resultaat.startswith(verwachtingbegin)
  assert resultaat.endswith(verwachtingeinde)
