#Python libraries 
from typing import Text
from flask import Flask, json, request
from pymessenger import Bot
from datetime import date
from pymongo import MongoClient
from saveConversation import Conversations

#################################################****************PACKAGES DE DIALOGFLOW***********************#############################
from os import environ
import dialogflow
from google.api_core.exceptions import InvalidArgument
#################################################***************APPLICATION******************#############################

app = Flask(__name__)
ACCESS_TOKEN = environ['ACCESS_TOKEN']
VERIFY_TOKEN = environ['VERIFY_TOKEN']
bot = Bot(ACCESS_TOKEN)

################################################***************LES CLEES DE DIALOGFLOW**************#########################


DIALOGFLOW_PROJECT_ID = environ['DIALOGFLOW_PROJECT_ID']
DIALOGFLOW_LANGUAGE_CODE = 'fr'
SESSION_ID = environ['SESSION_ID']
##############################################**************CONNECTION AVEC ATLAS MANGODB************#########################
def configureDataBase():
    client = MongoClient(environ['CONNECTION'])
    return client['db_conversation']
db = configureDataBase()
log = Conversations.Log()

#Nous recevrons des messages que Facebook envoie à notre bot à ce point de terminaison
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Avant d'autoriser les gens à envoyer un message à votre bot, Facebook a mis en place un jeton de vérification
        qui confirme que toutes les demandes que votre bot reçoit proviennent de Facebook""" 
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #si la demande n'a pas été reçue, il doit s'agir de POST et nous pouvons simplement renvoyer un message à l'utilisateur
    else:
        # Obtenir le message qu'un utilisateur a envoyé au bot
       output = request.get_json()
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                #ID Facebook Messenger pour l'utilisateur afin que nous sachions où renvoyer la réponse
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    text = message['message'].get('text')
                    res = process_message(text)
                    send_message(recipient_id,res)
                    info = bot.get_user_info(recipient_id, fields=None)
                    nom = info.get("last_name")
                    prenom = info.get("first_name")
                    photo = info.get("profile_pic")
                log.saveConversations(recipient_id,text,res,db)       
                log.saveInformation(recipient_id,nom,prenom,photo,db)
    return "Message Processed"


def verify_fb_token(token_sent):
    #prendre le jeton envoyé par facebook et vérifier qu'il correspond au jeton de vérification que vous avez envoyé
    #s'il correspondent autoriser la requete, sinon renvoyer une erreur
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


#fonction de traitement du message reçu
def process_message(text):
    formatted_message = text.lower()
    if formatted_message:
        text_to_be_analyzed = formatted_message
        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
        text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
        query_input = dialogflow.types.QueryInput(text=text_input)
        try:
            response = session_client.detect_intent(session,query_input)
        except InvalidArgument:
            raise
        response_sent_text = response.query_result.fulfillment_text
        #intent = response.query_result.intent.display_name
        #parameters = response.query_result.parameters
    return response_sent_text

#utilise PyMessenger pour envoyer une réponse à l'utilisateur
def send_message(recipient_id, response):
    #envoie à l'utilisateur le message texte fourni via le paramètre de réponse d'entrée
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == "__main__":
    app.run()
