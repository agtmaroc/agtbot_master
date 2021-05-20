from flask import Flask, request, Response
import requests, json, random, os
app = Flask(__name__)

# env_variables
# token to verify that this bot is legit
verify_token = 'UNIQE_TOKEN' #os.getenv('VERIFY_TOKEN', None)
# token to send messages through facebook messenger
access_token = 'EAACRZB81tqu0BANSFYFaLgoLDCnWS3cZCOhln9c1uyh3Y8oMCtqJvveAW86f505BcYYKfGoyIoZA5TUOnQm5Vlgzm5DQU4UAsuQSDEsTYcLTZCt9bhOQo3krhXYzFwVc8U1jTQg7ltNWs9Atmkt1K0k43xSRD0SCZASA2DzSHkFndmCgVGN3p'#os.getenv('ACCESS_TOKEN', None)

@app.route('/webhook', methods=['GET'])
def webhook_verify():
    if request.args.get('hub.verify_token') == verify_token:
        return request.args.get('hub.challenge')
    return "Wrong verify token"

@app.route('/webhook', methods=['POST'])
def webhook_action():
    data = json.loads(request.data.decode('utf-8'))
    for entry in data['entry']:
        user_message = entry['messaging'][0]['message']['text']
        user_id = entry['messaging'][0]['sender']['id']
        response = {
            'recipient': {'id': user_id},
            'message': {}
        }
        response['message']['text'] = handle_message(user_id, user_message)
        r = requests.post(
            'https://graph.facebook.com/v2.6/me/messages/?access_token=' + access_token, json=response)
    return Response(response="EVENT RECEIVED",status=200)

@app.route('/webhook_dev', methods=['POST'])
def webhook_dev():
    # custom route for local development
    data = json.loads(request.data.decode('utf-8'))
    user_message = data['entry'][0]['messaging'][0]['message']['text']
    user_id = data['entry'][0]['messaging'][0]['sender']['id']
    response = {
        'recipient': {'id': user_id},
        'message': {'text': handle_message(user_id, user_message)}
    }
    return Response(
        response=json.dumps(response),
        status=200,
        mimetype='application/json'
    )

def handle_message(user_id, user_message):
    # DO SOMETHING with the user_message ... ¯\_(ツ)_/¯
    return "Hello "+user_id+" ! You just sent me : " + user_message

@app.route('/privacy', methods=['GET'])
def privacy():
    # needed route if you need to make your bot public
    return "This facebook messenger bot's only purpose is to [...]. That's all. We don't use it in any other way."

@app.route('/', methods=['GET'])
def index():
    return "Hello there, I'm a facebook messenger bot."

if __name__ == '__main__':
    app.run()
