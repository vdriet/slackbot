""" testen voor de slackbot """
import unittest
from unittest.mock import patch, MagicMock
import pytest

import os

@pytest.fixture
def mock_env_slack_id(monkeypatch):
  monkeypatch.setenv("SLACK_ID_RASPBOT", "DUMMY")


def test_help_leeg(mock_env_slack_id):
  from slackbot import slackbot

  response = slackbot.message_help([])
  assert len(response) > 300

def test_help_enkel(mock_env_slack_id):
  from slackbot import slackbot

  tekst = 'enkel'
  response = slackbot.message_help([tekst])
  assert response == tekst

def test_help_meer(mock_env_slack_id):
  from slackbot import slackbot

  input = ['meer', 'tekst', 'samen']
  response = slackbot.message_help(input)
  assert response == 'meer tekst samen'
