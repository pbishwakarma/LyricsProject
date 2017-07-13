# Author: 	Prajal Bishwakarma
# Created:	7/12/2017


import re, urllib.parse, urllib.request
from xml.dom import minidom

class Song():

	def __init__(self, title=None, artist=None):
		self.artist = artist
		self.title = title
		self.url = None
		self.lyrics = None



	def __removeTags(self, html):
		# intros
		html = html.replace("<br>", "\n").replace("<br />", "\n")

		# remove html tags.
		p = re.compile(r'<.*?>')
		html = p.sub('', html)

		return html

	# Make url string
	def __makeUrl(self):


		info = {'artist': self.artist,
				'song': self.title
				}
		temp = {}
		for key in info:
			temp[key] = info[key].encode("utf-8")

		url = "http://api.chartlyrics.com/apiv1.asmx/SearchLyricDirect?" + urllib.parse.urlencode(temp)

		return url


	# Download lyrics from url
	def __download(self):

		self.url = self.__makeUrl()

		data = urllib.request.urlopen(self.url).read()

		lyrics = ""

		if data != "":

			dom = minidom.parseString(data)

			for item in dom.getElementsByTagName("Lyric"):
				lyrics += self.__removeTags(item.toxml()) + "\n"

		lyrics = lyrics.strip()

		self.lyrics = lyrics


	# Get methods
	def getArtist(self):
		return self.artist

	def getTitle(self):
		return self.title

	def getUrl(self):
		return self.url

	def getLyrics(self):
		if self.lyrics is not None:
			return self.lyrics
		else:
			self.__download()
			return self.lyrics

	def __str__(self):
		return "'" + str(self.title) + "' by " + str(self.artist)


def main():

	s1 = Song("Swimming Pools", "Kendrick Lamar")
	print(s1.getLyrics())

if __name__ == '__main__':
	main()