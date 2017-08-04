# Author: 	Prajal Bishwakarma
# Created:	7/12/2017
#

import requests
import time
import base64
from bs4 import BeautifulSoup
from keys import GENIUS_API_KEY
from keys import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
import pickle
import sys
import json

import re, urllib.parse, urllib.request

OFFLINE = True
BEARER = 'BQBil1KHhgDPeeEYURpxBIx6Fjhhl5_27Zs_9Nrqf6yh24YhJ25E6m4PwQzZDgPIbpYy0tp2IymaCK1aO5FzCQ'

class SpotifyTokenError(Exception):
	"""
	Custom exception to handle validity and excistence of Bearer token
	"""
	def __init__(self, message):
		"""
		Initialize the error

		Params:
		message - message to return upon raising of error (str)
		"""
		self.message = message

class _Token(object):

	def __init__(self, tok_type, token, exp_time=None):

		self.type = tok_type
		self.token = token
		self.exp_time = exp_time

	def getToken(self):
		return self.token

	def isExpired(self):
		if self.exp_time:
			return (self.exp_time - time.time()) < 0
		else:
			return False


class _Song(object):

	def __init__(self, title=None, artist=None, url=None, lyrics=None):
		self.title = title
		self.artist = artist
		self.url = url
		self.lyrics = lyrics

	# setters
	def setTitle(self, title):
		self.title = title

	def setArtist(self, artist):
		self.artist = artist

	def setLyrics(self, lyrics):
		self.lyrics = lyrics

	# getters
	def getTitle(self):
		return self.titles

	def getArtist(self):
		return self.artist

	def getLyrics(self):
		return self.lyrics

	def getUrl(self):
		return self.url
		

	def __str__(self):
		return "'" + self.title + "' " + "by " + self.artist




class SpotifyScraper(object):
	"""
	Scrapes the Spotify API to retrive an artist's full discography.
	Uses Client Credentials protocol to authorize application.
	"""

	BASE_URL = 'https://api.spotify.com'
	API_VERSION = '/v1'
	SEARCH_URL = BASE_URL + API_VERSION + '/search'
	

	

	def __init__(self, client_id, client_secret):
		self.id = client_id
		self.secret = client_secret
		self.token = None


	def _requestToken(self):
		"""
		Requests an authorization token from Spotify API.

		Returns:
		a json object with token and expiration time
		"""

		AUTH_URL ='https://accounts.spotify.com/api/token'

		data = {'grant_type': 'client_credentials'}

		encoded = base64.b64encode((self.id + ':' + self.secret).encode('utf-8'))
		headers = {'Authorization': 'Basic %s' % encoded.decode('utf-8')}

		return requests.post(AUTH_URL, data=data, headers=headers).json()

	def _get_stored_token(self):
		"""
		Retrieve and return the token from storage if available if not return None
		"""

		try:
			file = open('token.json')
		except FileNotFoundError:
			return None
		else:
			token_info = json.load(file)
			return(_Token('Spotify', token_info[0], token_info[1]))

	def authorize(self):
		"""
		Authorize scraper
		"""
		print('Authorizing...')
		try:
			self.token = self._makeAccessToken()
		except SpotifyTokenError:
			pass

	def _makeAccessToken(self):
		"""
		Makes Token object after requesting token.
		Stores token object in self.token attribute
		"""
		self.token = self._get_stored_token()

		if not self.token or self.token.isExpired():
			response = self._requestToken()
			tok = response['access_token']
			exp_time = int(time.time()) + int(response['expires_in'])

			with open('token.json', 'w') as file:
				json.dump([tok, exp_time], file)

			self.token = _Token("Spotify", tok, exp_time)
		else:
			raise SpotifyTokenError("Token already exists and is not expired")

	def _getArtistID(self, artist):
		"""
		Searches API for an artist's name and returns their ID.

		Params:
		artist -- artist's name (str)

		Returns:
		hit['id'] -- artist's ID (str)
		"""

		if not self.token:
			raise SpotifyTokenError('Authorization token not available. Try after authorizing')

		else:
			headers = {'Authorization': 'Bearer ' + self.token.getToken()}
			data = {'q' : artist, 'type' : 'artist' }

			res = requests.get(self.SEARCH_URL, params=data, headers=headers).json()

			for hit in res['artists']['items']:
				if hit['name'].lower() == artist.lower():
					return hit['id']

	def _getAlbums(self, artist_id):
		"""
		Searches API for an artist and returns all of their albums

		Params:
		artist_id -- artist's ID (str)

		Returns:
		albums -- dictionary with album names (str) as keys and list of album ids (str) as values
		"""
		albums = {}

		url = self.BASE_URL + self.API_VERSION + '/artists/%s/albums' % (artist_id)
		headers = {'Authorization': 'Bearer ' + self.token.getToken()}
		data = {'album_type':['album', 'single']}

		res = requests.get(url, params=data, headers=headers).json()

		for hit in res['items']:
			if hit['name'] not in albums:
				albums[hit['name']] = [hit['id']]
			else:
				albums[hit['name']].append(hit['id'])
			
		return albums



	def _getAllSongs(self, albums):
		"""
		Searches API for artist and returns all of their available songs on spotify

		Params:
		albums -- Dictionary wiht album names (str) as keys and album id (str) as values

		Returns:
		songs -- a list of song names (str) 
		"""
		songs = []
		headers = {'Authorization': 'Bearer ' + self.token.getToken()}
		data = {}

		for album in albums:
			for album_id in albums[album]:
				url = self.BASE_URL + self.API_VERSION + '/albums/%s/tracks' % (album_id)
				res = requests.get(url, params=data, headers=headers).json()

				for hit in res['items']:
					if hit['name'] not in songs:
						songs.append(hit['name'])

		return songs


	def getArtistDisc(self, artist):
		"""
		Searches the API for an artist and compiles all of their available songs as primary artist

		Param:
		artist -- artist name (str)

		Returns:
		disc -- a list of song names (str)
		"""
		print('Searching Spotify for artist...')
		artist_id = self._getArtistID(artist)
		albums = self._getAlbums(artist_id)
		songs = self._getAllSongs(albums)

		return songs










class GeniusScraper(object):

	BASE_URL = "https://api.genius.com"
	SEARCH_URL = BASE_URL + "/v1/search"



	def __init__(self, bearer):
		self.bearer = bearer
		self.token = None


	def makeAccessToken(self):
		self.token = _Token("Genius", self.bearer)


	def _getUrl(self, artist, title):

		data = {'q': title}
		headers = {'Authorization': 'Bearer ' + self.token.getToken()}

		res = requests.get(self.SEARCH_URL, data=data, headers=headers).json()

		for hit in res["response"]["hits"]:
			if hit["result"]["primary_artist"]["name"].lower() == artist.lower():
				return hit["result"]["url"]
		else:
			return None


	def _getLyrics(sefl, url):
		page = requests.get(url)
		html = BeautifulSoup(page.text, "html.parser")

		[h.extract() for h in html('script')]

		lyrics = html.find("div", class_="lyrics").get_text()

		return lyrics


	def _clean(self, text):
		skip1, skip2 = 0, 0
		ret = ''

		for char in text:
			if char == '[':
				skip1 += 1
			elif char == '(':
				skip2 += 1
			elif char == ']':
				skip1 -= 1
			elif char == ')':
				skip2 -= 1
			elif skip1 == 0 and skip2 == 0:
				ret += char

		return ret

	def makeSongs(self, artists):

		songs = []

		for artist in artists:
			for song_title in artists[artist]:

				url = self._getUrl(artist, song_title)

				if url is not None:
					lyrics = self._clean(self._getLyrics(url))
				else:
					lyrics = None
				
				songs.append(_Song(song_title, artist, url, lyrics))

		return songs

def getXXLFreshmen():

	wikiurl = 'https://en.wikipedia.org/wiki/XXL_(magazine)#XXL_Annual_Freshman_List'
	header = {'User Agend': 'Mozilla/5.0'}
	page = urllib.request.urlopen(wikiurl)
	html = BeautifulSoup(page, 'lxml')
	
	table = html.find("table", { "class": "sortable wikitable"})

	xxl_lists = {}
	year = ''
	artists = ''
	for row in table.findAll('tr'):
		cell = row.findAll('td')

		if len(cell) == 2:
			year = str(cell[0].find(text=True))
			temp = cell[1].findAll(text=True)

			artists = [str(text) for text in temp if text[0] not in '[,. ']

			xxl_lists[year] = {artist: [] for artist in artists}

	
	return xxl_lists





# def main():
# 	if sys.argv[1] == 'offline' or sys.argv[1] == '-o':
# 		with open('songs.p', 'rb') as f:
# 			songs = pickle.load(f)

# 		for song in songs:
# 			print(song.getLyrics())

# 	else:
# 		xxl_2017 = {"Kamaiyah": ['Break You Down'],
# 				"A Boogie wit da Hoodie": ['Drowning'],
# 				"PnB Rock": ['Selfish'],
# 				"MadeinTYO": ['Uber Everywhere'],
# 				"Playboi Carti": ['Magnolia'],
# 				"Aminé": ['Caroline'],
# 				"Kap G": ['Girlfriend'],
# 				"Kyle": ['iSpy'],
# 				"Ugly God": ['Water'],
# 				"XXXTentacion": ['Look at Me']
# 				}

# 		gScrape = GeniusScraper(GENIUS_API_KEY)
# 		gScrape.makeAccessToken()

# 		songs = gScrape.makeSongs(xxl_2017)

# 		pickle.dump(songs, open("songs.p", 'wb'))

# 		# with open('songs.txt', 'w') as s:
# 		# 	for song in songs:
# 		# 		s.write(str(song))
# 		# 		s.write(song.getLyrics())


def main():

	if not OFFLINE:
		xxl = getXXLFreshmen()
		pickle.dump(xxl, open('xxl.p', 'wb'))
	else:
		with open('xxl.p', 'rb') as file:
			xxl = pickle.load(file)

		spot = SpotifyScraper(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
		spot.authorize()

		# for year in xxl:
		# 	for artist in xxl[year]:
		# 		spot.getArtistID(artist)

		kdot = spot.getArtistDisc('Kendrick Lamar')
		print(kdot)

	# xxl = getXXLFreshmen()
	# pickle.dump(xxl, open('xxl.p', 'wb'))




if __name__ == '__main__':
	main()

























