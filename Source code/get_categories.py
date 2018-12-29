from pickle import dump, HIGHEST_PROTOCOL
from nltk.corpus import reuters

orig = {}

for i in range(21576):
	if i <=14818:
		categs = reuters.categories("training/" + str(i))
		if(len(categs) != 0):
			orig.update({i : categs})
	else:
		categs = reuters.categories("test/" + str(i))
		if(len(categs) != 0):
			orig.update({i : categs})

with open("categories", "wb") as c:
	dump(orig, c, HIGHEST_PROTOCOL)

l = []
for i in orig.values():
	l.extend(i)

l = sorted(list(set(l)))

inverted = {i:[] for i in l}
for i in range(21576):
	if i <=14818:
		categs = reuters.categories("training/" + str(i))
	else:
		categs = reuters.categories("test/" + str(i))
	for j in categs:
		inverted[j].append(i)

with open("inverted_categ_dict", "wb") as ic:
	dump(inverted, ic, HIGHEST_PROTOCOL)