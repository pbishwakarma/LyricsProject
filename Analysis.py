import pickle
import json
import timeit
import pprint

from Song import _Song

def main():

	pp = pprint.PrettyPrinter(indent = 4)

	with open('songs.p', 'rb') as file:
		songs = pickle.load(file)

	ct = 0
	artists = {}
	for song in songs:
		artist = song.getArtist()
		if artist not in artists:
			artists[artist] = 1
		else:
			artists[artist] += 1

		lyr = song.getLyrics()
		if lyr is not None:
			ct += 1
		if artist == "XXXTentacion":
			print(lyr)

	pp.pprint(artists)
	print(ct)





if __name__ == '__main__':
	main()