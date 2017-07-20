#!/usr/bin/python

import requests
import base64
import json
from flask import Flask

# Spotify client info
from keys import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET


def requestToken(client_id, client_secret):


	AUTH_URL ='https://accounts.spotify.com/api/token'

	data = {'grant_type': 'client_credentials'}

	encoded = base64.b64encode((client_id + ':' + client_secret).encode('utf-8'))
	headers = {'Authorization': 'Basic %s' % encoded.decode('utf-8')}

	return requests.post(AUTH_URL, data=data, headers=headers).json()


	

def main():

	response = requestToken(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
	print(response)



if __name__ == '__main__':
	# app.run()
	main()


