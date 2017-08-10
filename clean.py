import json
from tqdm import tqdm


def _clean(text):
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


with open('xxl_complete.json', 'r') as file:
	xxl = json.load(file)


ct = 0

for year in tqdm(xxl):
	for artist in xxl[year]:
		for song in xxl[year][artist]:
			if 'feat' in song.lower():
				song = _clean(song)


print(ct)

