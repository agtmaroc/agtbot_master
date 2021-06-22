# doing necessary imports
from flask import Flask, render_template, request, jsonify, make_response
import requests
import pymongo
import json
from os import environ
from pymongo import MongoClient
from saveConversation import Conversations



app = Flask(__name__)  # initialising the flask app with the name 'app'

def configureDataBase():
    client = MongoClient(environ['CONNECTION'])
    return client['db_conversation']
db = configureDataBase()
log = Conversations.Log()

# geting and sending response to dialogflow
@app.route('/webhook', methods=['POST'])

def webhook():
    req = request.get_json(silent=True, force=True)
    res = processRequest(req)
    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


# processing the request from dialogflow

def processRequest(req):
    log = Conversations.Log()
    sessionID = req.get('responseId')
    result = req.get("queryResult")
    intent = result.get("intent").get('displayName')
    query_text = result.get("queryText")
    reponse = result.get("fulfillmentText")
    parameters = result.get("parameters")
    nom = parameters.get("nom")
    email = parameters.get("email")
    numero = parameters.get("numero")
    sender_id = req.get("originalDetectIntentRequest").get("payload").get("data").get("sender").get("id")
    db = configureDataBase()

    if intent == 'oui':
        records = db.info_personne
        if(records.find({"userID":sender_id}).count() == 0):
            return{
                "fulfillmentMessages":[
                  {
                     "text":"not anymore"
                  }
                                      ]
                  }
        else:
            log.saveInformation(sender_id,nom,numero,email,db)
            return 200
    elif intent != 'oui':
        log.saveConversations(sender_id,query_text,reponse,db)
        return 200





if __name__ == '__main__':
    app.run()

    
    
