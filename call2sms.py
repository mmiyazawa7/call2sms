
# coding: utf-8

# In[ ]:


from flask import Flask,request, Response,session
import requests
import json
import nexmo
import datetime
from base64 import urlsafe_b64encode
import os
import calendar
# from jose import jwt
import jwt # https://github.com/jpadilla/pyjwt -- pip3 install PyJWT
import coloredlogs, logging
from uuid import uuid4

# test

# for heroku, please put all env parameters to 'Config Vars` in heroku dashboard
# from dotenv import load_dotenv
# dotenv_path = join(dirname(__file__), '.env')
# load_dotenv(dotenv_path)

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)

api_key = os.environ.get("API_KEY") 
api_secret = os.environ.get("API_SECRET")
application_id = os.environ.get("APPLICATION_ID")

private_key = os.environ.get("PRIVATE_KEY")

# keyfile = "private.key"

url = "https://api.nexmo.com/v1/calls"

webhook_url = os.environ.get("WEBHOOK_URL")

web_port = os.environ.get("WEB_PORT")

virtual_number = os.environ.get("LVN")

digital_human_url = os.environ.get("DIGITAL_HUMAN_URL")


session={}
client_sms = nexmo.Client(key=api_key, secret=api_secret)

@app.route('/answer',methods=['GET', 'POST'])
def japanivr():

    arg_to = request.args['to']
    arg_from = request.args['from']

    session['to'] = arg_to
    session['from'] = arg_from

    logger.debug('From: %s', arg_from)
    logger.debug('To: %s', arg_to)

    ncco=[{
	        "action": "talk",
	        "text": "　　こんにちは。デジタルヒューマンにおつなぎするには、１とシャープを、ゔぉねーじに関する情報は２とシャープを入力してください。",
            "bargeIn": "true",
	        "voiceName": "Mizuki"

	      },
          {
            "action": "input",
            "timeOut": "30",
            "submitOnHash": "true",
            "eventUrl": [ webhook_url + "/dtmfresponse"]
            }]
    js=json.dumps(ncco)
    resp=Response(js, status=200, mimetype='application/json')
    print(resp.data)
    return resp


@app.route('/dtmfresponse',methods=['GET', 'POST'])
def dtmfresponse():

    currentDT = datetime.datetime.now()
    date =currentDT.strftime("%Y-%m-%d %H:%M:%S")

    webhookContent = request.json
    print(webhookContent)
    try:
        result = webhookContent['dtmf']
    except:
        pass

    logger.debug("The User enter: " + str(result) + "\n")
    logger.debug(date)

    if result == '1':

        sms_text = "デジタルヒューマンに接続するためのURLは" + digital_human_url + "です"

        
        response_SMS = client_sms.send_message({'from': 'VonageJapan', 'to': session['from'] , 'text': sms_text})

        logger.debug(response_SMS)
        logger.debug(sms_text)

        ncco = [
                 {
            "action": "talk",
            "text": "デジタルヒューマンにお繋ぎするためのURLをSMSでお送りしましたので、そちらをクリックして接続してください",
            "voiceName": "Mizuki"
        }
              ]
        js = json.dumps(ncco)
        resp = Response(js, status=200, mimetype='application/json')
        logger.debug('Response NCCO with Ryu number')
        print(resp)
        return resp
    elif result == '2':
        sms_text = "ヴォネージに関する情報は、こちらを参照してください。https://www.vonagebusiness.jp/communications-apis/ "

        response_SMS = client_sms.send_message({'from': 'NexmoJapan', 'to': session['from'], 'text': sms_text})
        logger.debug(response_SMS)
        logger.debug(sms_text)

        ncco = [
            {
            "action": "talk",
            "text": "ヴォネージに関する情報のURLをSMSでお送りしましたので、そちらを確認してください",
            "voiceName": "Mizuki"
        }
        ]

        js = json.dumps(ncco)
        resp = Response(js, status=200, mimetype='application/json')
        logger.debug('Response NCCO with Miya number')
        print(resp)
        return resp
    else:
        ncco = [
            {
                "action": "talk",
                "text": "　入力が確認できません。もう一度入力してください　",
                "voiceName": "Mizuki"
            },
            {
                "action": "notify",
                "payload": {
                    "dtmf_status": "uncompleted"
                },                
                "eventUrl": [webhook_url+"/answer"],
                "eventMethod": "POST"
            }
        ]
        js = json.dumps(ncco)
        resp = Response(js, status=200, mimetype='application/json')
        logger.debug('Response NCCO to record call')
        print(resp)
        return resp
    return "success"

@app.route('/event', methods=['GET', 'POST', 'OPTIONS'])
def display():
    r = request.json
    print(r)
    return "OK"


if __name__ == '__main__':
    app.run(port=web_port)

