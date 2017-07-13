# Author: 	Prajal Bishwakarma
# Created:	7/12/2017
#

import requests
from bs4 import BeautifulSoup
from keys import GENIUS_API_KEY 



class _Song(object):

	def __init__(self, title=None, artist=None, url=None):
		self.title = title
		self.artist = artist
		self.url = url
		self.lyrics = None


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
		return "'" + self.title + "'" + "by " + self.artist


base = "https://api.genius.com"
headers = {'Authorization': 'Bearer ' + GENIUS_API_KEY}

search_url = base + "/search"

song = "Famous"
artist = "Kanye West"


data = {'q': song}

response = requests.get(search_url, data=data, headers=headers)

res = response.json()


# for hit in res["response"]["hits"]:
# 	print(hit["result"]["full_title"])


xxl_2017 = {"Kamaiyah": ['Break You Down'],
			"A Boogie wit da Hoodie": ['Drowning'],
			"PnB Rock": ['Selfish'],
			"MadeinTYO": ['Uber Everywhere'],
			"Playboi Carti": ['Telephone Calls'],
			"Aminé": ['Caroline'],
			"Kap G": ['Girlfriend'],
			"Kyle": ['iSpy'],
			"Ugly God": ['Water'],
			"XXXTentacion": ['Look at Me']
			}

songs_2017 = {}



for hit in res["response"]["hits"]:
	if hit["result"]["primary_artist"]["name"].lower() == artist.lower():
		song_title = hit["result"]["title"]
		song_artist = hit["result"]["primary_artist"]["name"]
		song_url = hit["result"]["url"]

		songs_2017[song_title] = _Song(song_title, song_artist, song_url)


for key in songs_2017:
	temp_url = songs_2017[key].getUrl()
	page = requests.get(temp_url)
	html = BeautifulSoup(page.text, "html.parser")

	[h.extract() for h in html('script')]

	lyrics = html.find("div", class_="lyrics").get_text()

	print(lyrics)


















