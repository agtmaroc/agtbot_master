
from typing import Text
from flask import Flask, json, request
from pymessenger import Bot
#####################################################
import json
import os
from os import environ
import dialogflow
from google.api_core.exceptions import InvalidArgument
######################################################

app = Flask(__name__)
PAGE_ACCESS_TOKEN = 'EAACBNZAZAIEZBEBABhai7xJ2GB7orSr6BPvTtDglSnZBSLNGmhbyvyvvHWVhiLRhuQXgxBLZChjWSTMdM4mSGTvMPY3t61NK3tBRTYkrEXJmGBiQoXdZBZCTEu859OvIgl8zvVVvpLhHzSla404xiCQa6moVElXjHZBBkRuv1sp7LUytoCNghbt8'

bot = Bot(PAGE_ACCESS_TOKEN)

VERIFY_TOKEN ='UNIQE_TOKEN'
#################################################################################################
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'private_key.json'

DIALOGFLOW_PROJECT_ID = 'test-wj9j'
DIALOGFLOW_LANGUAGE_CODE = 'fr'
SESSION_ID = 'me'
#########################################################################################################

def process_message(text):
    formatted_message = text.lower()
    if formatted_message:
        text_to_be_analyzed = formatted_message
        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
        text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
        query_input = dialogflow.types.QueryInput(text=text_input)
        try:
            response = session_client.detect_intent(session=session, query_input=query_input)
        except InvalidArgument:
            raise
        response_sent_text = response.query_result.fulfillment_text
        response = response_sent_text
    return response

@app.route('/', methods=["POST", "GET"])
def webhook():
    if request.method == "GET":
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        else:
            return "Hello"

    elif request.method == "POST":
        payload = request.json
        event = payload['entry'][0]['messaging']

        for msg in event:
            text = msg['message']['text']
            sender_id = msg['sender']['id']

            response = process_message(text)
            bot.send_text_message(sender_id, response)

        return "Message received"
    else:
        return "200"




if __name__ == '__main__':
    app.run()
