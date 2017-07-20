# Author: 	Prajal Bishwakarma
# Created:	7/12/2017
#

import requests
from bs4 import BeautifulSoup
from keys import GENIUS_API_KEY
from keys import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
import pickle
import sys



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


base = "https://api.genius.com"
token = 'Bearer ' + GENIUS_API_KEY
HEADERS = {'Authorization': token}
SEARCH_URL = base + "/search"




# for hit in res["response"]["hits"]:
# 	print(hit["result"]["full_title"])



songs_2017 = {}



# for hit in res["response"]["hits"]:
# 	if hit["result"]["primary_artist"]["name"].lower() == artist.lower():
# 		song_title = hit["result"]["title"]
# 		song_artist = hit["result"]["primary_artist"]["name"]
# 		song_url = hit["result"]["url"]

# 		songs_2017[song_title] = _Song(song_title, song_artist, song_url)


# for key in songs_2017:
# 	temp_url = songs_2017[key].getUrl()
# 	page = requests.get(temp_url)
# 	html = BeautifulSoup(page.text, "html.parser")

# 	[h.extract() for h in html('script')]

# 	lyrics = html.find("div", class_="lyrics").get_text()

# 	print(lyrics)


def getUrl(artist, title):

	data = {'q': title}

	res = requests.get(SEARCH_URL, data=data, headers=HEADERS).json()

	for hit in res["response"]["hits"]:

		if hit["result"]["primary_artist"]["name"].lower() == artist.lower():
			return hit["result"]["url"]

	else:
		return None

def getLyrics(url):
	page = requests.get(url)
	html = BeautifulSoup(page.text, "html.parser")

	[h.extract() for h in html('script')]

	lyrics = html.find("div", class_="lyrics").get_text()

	return lyrics


def clean(text):
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

def makeSongs(artists):

	songs = []

	for key in artists:

		artist = key
		for song_title in artists[key]:

			url = getUrl(artist, song_title)

			if url is not None:
				lyrics = clean(getLyrics(url))
			else:
				lyrics = None
			
			songs.append(_Song(song_title, artist, url, lyrics))

	return songs


def main():
	if sys.argv[1] == 'offline' or sys.argv[1] == '-o':
		with open('songs.p', 'rb') as f:
			songs = pickle.load(f)

		for song in songs:
			print(song.getLyrics())

	else:
		xxl_2017 = {"Kamaiyah": ['Break You Down'],
				"A Boogie wit da Hoodie": ['Drowning'],
				"PnB Rock": ['Selfish'],
				"MadeinTYO": ['Uber Everywhere'],
				"Playboi Carti": ['Magnolia'],
				"Aminé": ['Caroline'],
				"Kap G": ['Girlfriend'],
				"Kyle": ['iSpy'],
				"Ugly God": ['Water'],
				"XXXTentacion": ['Look at Me']
				}

		songs = makeSongs(xxl_2017)

		pickle.dump(songs, open("songs.p", 'wb'))

		# with open('songs.txt', 'w') as s:
		# 	for song in songs:
		# 		s.write(str(song))
		# 		s.write(song.getLyrics())



if __name__ == '__main__':
	main()



























