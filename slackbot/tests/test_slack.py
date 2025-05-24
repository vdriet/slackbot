# """ testen voor de slackbot message """
# from unittest.mock import patch
#
# import pytest
#
#
# @pytest.fixture
# def mock_environment(monkeypatch):
#   monkeypatch.setenv("SLACK_BOT_TOKEN", "DUMMY")
#   monkeypatch.setenv("MAIL_USER_DUMMY", "DUMMY")
#   monkeypatch.setenv("MAIL_PASS_DUMMY", "DUMMY")
#   monkeypatch.setenv("MAIL_HOST", "DUMMY")
#
#
# def say(text):
#   return text
#
#
# @patch('slack_bolt.App')
# def test_handle_message(mock_app, mock_environment):
#   import slackbot
#
#   bericht = {'user': 'peter'}
#   verwachting = ''
#   resultaat = slackbot.handle_message(bericht, say)
#   assert verwachting == resultaat
