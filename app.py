# doing necessary imports
from flask import Flask, render_template, request, jsonify, make_response
import requests
import pymongo
import json
import os
from pymongo import MongoClient
from saveConversation import Conversations



app = Flask(__name__)  # initialising the flask app with the name 'app'

def configureDataBase():
    client = MongoClient("mongodb+srv://agt:agt@cluster.pyiww.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
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
    sender_id = req.get("originalDetectIntentRequest").get("payload").get("data").get("sender")
    db = configureDataBase()

    if intent == 'oui':
        log.saveInformation(sessionID,nom,email,numero,db)
        return 200
    elif intent != 'oui':
        log.saveConversations(sessionID,query_text,sender_id,db)
        return 200





if __name__ == '__main__':
    app.run()

    
    
