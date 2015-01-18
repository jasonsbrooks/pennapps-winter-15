from flask import (Flask, render_template, Response, request, 
    Blueprint, redirect, send_from_directory, send_file, jsonify, g, url_for)

from twilio.rest import TwilioRestClient
from twilio import twiml
import os
import time

splash = Blueprint('splash', __name__, template_folder="")

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Home function with no real purpose
@splash.route('/')
def home():
    return "Hello World."

# This is soley for testing
@splash.route('/call', methods=['GET'])
def call():
	call = client.calls.create(to="5166724605",
                           from_="2036664511",
                           url="http://browser.ngrok.com/send-swift-xml")
	print(call.sid)
	return "meow"

# Initialize a call with a twilio number.
@splash.route('/new-stream', methods=['POST'])
def initialize():
	print request.values
	resp = twiml.Response()
	with resp.gather(timeout=999, numDigits="1", action="/send-request-handler", method="POST") as g:
		g.say("Session activated.")
	return str(resp)

@splash.route('/send-request-handler', methods=['GET', 'POST'])
def sendRequest():
	recording_url = request.values.get("RecordingUrl", None)
	if recording_url:
		requestSiteFromAudioURL(recording_url)
	resp = twiml.Response()
	# play recording
	# print recording_url
	# resp = twiml.Response()
	# resp.record(finishOnKey='#', timeout=999)
	# resp.say("Goodbye.")
	return str(resp)

# @splash.route('/receive-data-handler', methods=['GET', 'POST'])
# def receiveRequest():
# 	resp = twiml.Response()


@splash.route('/send-swift-xml', methods=['POST'])
def swift():
	xml = '<?xml version="1.0" encoding="UTF-8"?><Response><Play>https://s3.amazonaws.com/noteable-paf14/f777cb906c7df6d5c3be7da3900877018018222c6418dd25a12dc3aa.wav</Play><Redirect/></Response>'
	return Response(xml, mimetype='text/xml')
