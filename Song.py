# Author: 	Prajal Bishwakarma
# Created:	7/12/2017
#

import requests
import time
from bs4 import BeautifulSoup
from keys import GENIUS_API_KEY
from keys import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
import pickle
import sys

import re, urllib.parse, urllib.request


class _Token(object):

	def __init__(self, tok_type, token, exp_time=None):
		self.type = tok_type
		self.token = token
		self.exp_time = exp_time

	def getToken(self):
		return self.token

	def isExpired(self):
		if not self.exp_time:
			return (time.time() - self.exp_time) > 0
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


	def __init__(client_id, client_secret):
		self.id = client_id
		self.secret = client_secret
		self.token = None


	def _requestToken():

		AUTH_URL ='https://accounts.spotify.com/api/token'

		data = {'grant_type': 'client_credentials'}

		encoded = base64.b64encode((self.id + ':' + self.secret).encode('utf-8'))
		headers = {'Authorization': 'Basic %s' % encoded.decode('utf-8')}

		return requests.post(AUTH_URL, data=data, headers=headers).json()

	def makeAccessToken():
		if not self.token or self.token.isExpired():
			response = self._requestToken()
			tok = response['access_token']
			exp_time = int(time.time()) + int(response['expires_in'])
			self.token = _Token("Spotify", tok, exp_time)
		else:
			raise SpotifyTokenError("Token already exists and is not expired")

	



class GeniusScraper(object):

	BASE_URL = "https://api.genius.com"
	SEARCH_URL = BASE_URL + "/search"



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
			year = cell[0].find(text=True)
			temp = cell[1].findAll(text=True)

			artists = [text for text in temp if text[0] not in '[,. ']

			xxl_lists[year] = {artist: [] for artist in artists}

	
	return xxl_lists


			# for item in cell:
			# 	print(item.findAll(text=True))
			# print(cell[1].findAll(text=True))







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
	# with open('songs.p', 'rb') as f:
	# 	songs = pickle.load(f)

	# 	for song in songs:
	# 		print(song.getLyrics())

	xxl = getXXLFreshmen()

if __name__ == '__main__':
	main()



























