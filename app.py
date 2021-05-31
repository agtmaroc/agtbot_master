#Python libraries that we need to import for our bot
from typing import Text
from flask import Flask, json, request
from pymessenger import Bot
from datetime import date
from pymongo import MongoClient
from saveConversation import Conversations

#####################################################
import json
import os
from os import environ
import dialogflow
from google.api_core.exceptions import InvalidArgument
######################################################

app = Flask(__name__)
ACCESS_TOKEN = 'EAAXI9pEEBREBAP1H2bOf9chq6GdPEW5SuCjQMJBIg72DzZBkabwQOWkIVomSQNZC7LtKI2KBfh9USIyscw93TmRpowyOJpqJTCnsDRZA6jKKYwl6dvPWJMZB9LQl0bb0i3PzzfTgEo4ur7DgLbo4LAnwmhSZAgL4D3gHHUrv8jPQzQ1qfZAQJYr2zbFCaiPXkZD'
VERIFY_TOKEN = 'UNIQE_TOKEN'
bot = Bot(ACCESS_TOKEN)

#################################################################################################
private_key = json.loads(environ['credential'])
environ['GOOGLE_APPLICATION_CREDENTIALS'] ='private_key'
DIALOGFLOW_PROJECT_ID = environ['DIALOGFLOW_PROJECT_ID']
DIALOGFLOW_LANGUAGE_CODE = 'fr'
SESSION_ID = environ['SESSION_ID']
#########################################################################################################
def configureDataBase():
    client = MongoClient("mongodb+srv://agt:agt@cluster.pyiww.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    return client['db_conversation']
db = configureDataBase()
log = Conversations.Log()

#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook.""" 
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
       output = request.get_json()
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    text = message['message'].get('text')
                    response_sent_text = process_message(text)
                    send_message(recipient_id, response_sent_text)
                log.saveConversations(recipient_id,text,response_sent_text,db)       
                
    return "Message Processed"


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'



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

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == "__main__":
    app.run()
