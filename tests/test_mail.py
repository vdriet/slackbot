""" testen voor de slackbot mailfuncties """
from unittest.mock import patch

import pytest


@pytest.fixture
def mock_environment(monkeypatch):
  monkeypatch.setenv("SLACK_ID_RASPBOT", "DUMMY")
  monkeypatch.setenv("MAIL_USER_DUMMY", "DUMMY")
  monkeypatch.setenv("MAIL_PASS_DUMMY", "DUMMY")
  monkeypatch.setenv("MAIL_HOST", "DUMMY")


def test_message_mail_leeg(mock_environment):
  import slackbot

  invoer = []
  verwachting = 'Gebruik mail <prefix>'
  resultaat = slackbot.message_mail(invoer)
  assert resultaat == verwachting


def test_message_mail_dubbel(mock_environment):
  import slackbot

  invoer = ['a', 'b']
  verwachting = 'Gebruik mail <prefix>'
  resultaat = slackbot.message_mail(invoer)
  assert resultaat == verwachting


def test_message_mail_alles(mock_environment):
  import slackbot

  invoer = ['alles']
  verwachting = 'ToDo'
  resultaat = slackbot.message_mail(invoer)
  assert resultaat == verwachting


def test_message_mail_no_env(mock_environment):
  import slackbot

  invoer = ['nodummy']
  verwachting = "Geen gegevens gevonden voor nodummy\n'MAIL_USER_NODUMMY'"
  resultaat = slackbot.message_mail(invoer)
  assert resultaat == verwachting
