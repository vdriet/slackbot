""" Bot voor slack """
import os
import sys
from slack_sdk.rtm_v2 import RTMClient
from google_trans_new import google_translator, google_trans_new

BOT_ID = 'U4QCBT18A'
# constants
AT_BOT = f'<@{BOT_ID}>'
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
        else :
            filelist = event.get('files', None)
            if filelist is None :
                response = 'Type "help" voor uitleg'
            else :
                for file in filelist :
                    ftype = file['filetype']
                    if ftype != 'text' :
                        response = 'Alleen bestanden met tekst kunnen worden vertaald'
                    else :
                        text = file['preview']
                        gtrans = google_translator()
                        translation = gtrans.translate(text, lang_src ='en', lang_tgt='nl')
                        # print(trans)
                        response = f'vertaling: [{translation}]'
    except google_trans_new.google_new_transError:
        print(f'ERR: {sys.exc_info()}')
        response = 'Fout bij vertalen'
    except:
        print(f'ERR: {sys.exc_info()}')
        response = f'Er is iets foutgegaan: {sys.exc_info()[0]}'

    web_client.chat_postMessage(
        channel=channel_id,
        text=response,
        thread_ts=thread_ts
    )

if __name__ == "__main__":
    rtm.start()
