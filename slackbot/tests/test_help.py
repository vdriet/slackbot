""" testen voor de slackbot helpfunctie """
import unittest
import pytest

@pytest.fixture
def mock_env_slack_id(monkeypatch):
  monkeypatch.setenv("SLACK_ID_RASPBOT", "DUMMY")


def test_help_leeg(mock_env_slack_id):
  from slackbot import slackbot

  resultaat = slackbot.message_help([])
  assert len(resultaat) > 300

def test_help_enkel(mock_env_slack_id):
  from slackbot import slackbot

  tekst = 'enkel'
  resultaat = slackbot.message_help([tekst])
  assert resultaat == tekst

def test_help_meer(mock_env_slack_id):
  from slackbot import slackbot

  invoer = ['meer', 'tekst', 'samen']
  resultaat = slackbot.message_help(invoer)
  assert resultaat == 'meer tekst samen'
