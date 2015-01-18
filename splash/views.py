from flask import (Flask, render_template, Response, request, 
    Blueprint, redirect, send_from_directory, send_file, jsonify, g, url_for)

from twilio.rest import TwilioRestClient
from twilio import twiml
import os

splash = Blueprint('splash', __name__, template_folder="")

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@splash.route('/')
def home():
    return "Hello World."

@splash.route('/call', methods=['GET'])
def call():
	call = client.calls.create(to="5166724605",
                           from_="2036664511",
                           url="http://browser.ngrok.com/send-swift-xml")
	print(call.sid)
	return "meow"

@splash.route('/new-stream', methods=['POST'])
def receive():
	print request.values
	resp = twiml.Response()
	with resp.gather(numDigits=1, timeout=100000, action="/handle-recording", method="POST") as g:
		g.say("To begin data stream, press any key.")
		# resp.record(maxLength="1000000000", action="/handle-recording", finishOnKey="#")
	return str(resp)

@splash.route('/handle-recording', methods=['GET', 'POST'])
def recording():
	resp = twiml.Response()
	recording_url = request.values.get("RecordingUrl", None)
	print recording_url
	resp = twiml.Response()
	resp.say("Goodbye.")
	return str(resp)

@splash.route('/send-swift-xml', methods=['POST'])
def swift():
	xml = '<?xml version="1.0" encoding="UTF-8"?><Response><Play>https://s3.amazonaws.com/noteable-paf14/7d679bbcdc8f1353865f6452fd3a9bc73e3f56daed1741bc201ba978.wav</Play><Redirect/></Response>'
	return Response(xml, mimetype='text/xml')
