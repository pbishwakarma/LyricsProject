#!/usr/bin/python

import requests
import base64
import json
from flask import Flask

# Spotify client info
from keys import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

# Spotify urls
BASE_URL = 'https://accounts.spotify.com'
TOKEN_URL = BASE_URL + '/api/token'
API_URL = 'https://api.spotify.com'


app = Flask(__name__)

@app.route("/")
def index():
	response = requestToken(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
	return str(response)

	
def requestToken(client_id, client_secret):


	AUTH_URL ='https://accounts.spotify.com/api/token'

	data = {'grant_type': 'client_credentials'}

	encoded = base64.b64encode(bytes(client_id + ':' +client_secret, 'utf-8'))
	headers = {'Authorization': 'Basic %s' % encoded}

	return requests.post(AUTH_URL, data=data, headers=headers).json()


	

def main():

	response = requestToken(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
	print(response)



if __name__ == '__main__':
	# app.run()
	main()


