from pickle import load, dump, HIGHEST_PROTOCOL
from utilities import load_vocab

with open('vocabulary', 'rb') as v:
	vocab = load(v).keys()

alphabets = 'abcdefghijklmnopqrstuvwxyz'

bigrams = {}
for i in alphabets:
	for j in alphabets:
		bigrams.update({i+j:[]})
	bigrams.update({i + '$':[]})


v = load_vocab()

for i in v.keys():
	bg = []
	for j in range(len(i) - 1):
		bg.append(i[j] + i[j+1])
	bg.append(i[len(i) - 1] + '$')
	bg = set(bg)
	for j in bg:
		if j in bigrams.keys():
			pl = bigrams[j][:]
			pl.append(i)
			bigrams[j] = pl
		else:
			pass

with open("bigrams", "wb") as b:
	dump(bigrams, b, HIGHEST_PROTOCOL)