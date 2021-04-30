# Call 2 SMS for Digital Human

This is sample application demo how to make Simple Voice IVR

This app is built using [Flask framework](http://flask.pocoo.org/) and require [Python3](https://www.python.org/)

## Prerequisite

You will need a few thins to get going with this app: 

- A [Nexmo](https://nexmo.com) Account
- A Nexmo Messages & Dispatch App [[set one up here]](https://dashboard.nexmo.com/messages/create-application)
- A Nexmo Voice App [[set one up here]](https://dashboard.nexmo.com/voice/create-application)
- To buy Phone Number for Voice App [[set one up here]](https://dashboard.nexmo.com/buy-numbers)


To install the Python client library using pip:

    pip install nexmo

To upgrade your installed client library using pip:

    pip install nexmo --upgrade

To rename .env_sample to .env and set parameter

## Running the demo


For demo, to run ngrok for webhook

    $ ngrok http 3000

    Forwarding                    https://xxxxxx.ngrok.io -> localhost:3000
    
Please set "https://xxxxxx.ngrok.io" to "WEBHOOK_URL" in .env file

    WEBHOOK_URL = "Your Base Webhook URL"

To run application

$ python3 ivr-sample.py
    
Webhook will be up and running using PORT:3000

## To deploy heroku

Install Heroku CLI Tool

    $ brew install heroku-toolbelt
    $ heroku login
    Enter your Heroku credentials.
    Email: [email]
    Password (typing will be hidden)
    Logged in as [email]
    
Deploy this App to Heroku

    $ git clone https://github.com/mmiyazawa7/ivr-sample-py.git
    $ heroku create (your heroku app name)
    $ git push heroku master
    
Setup env parameters to Config Vars in heroku

    Open 'https://dashboard.heroku.com/apps/(your heroku app name)/settings'
    Set `Concig Vars`
    
    API_KEY
    API_SECRET
    APPLICATION_ID      (Your Nexmo Voice Application ID)
    LVN                 (Your Nexmo Voice LVN)
    PRIVATE_KEY         (Your Provate Key)
    WEBHOOK_URL        (Webhook URL on heroku)
    WEB_PORT            (Web Port for this App)
    DIGITAL_HUMAN_URL = "Digital Human URL"
    
Monitor heroku logs

    $ heroku logs
    $ heroku logs --tail
    