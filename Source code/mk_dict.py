import simplejson
import nltk
from nltk.corpus import PlaintextCorpusReader
from pickle import dump, HIGHEST_PROTOCOL

orig = {}
for i in range(1, 14818):
	try:
		words_ = PlaintextCorpusReader(r'./nltk_data/corpora/reuters/training', str(i)).words()
		for j in words_:
			if j in orig.keys():
				j_list = orig[j]
				j_list.append(str(i))
				orig.update({j:list(set(j_list))})
			else:
				orig.update({j:[str(i)]})
	except ValueError:
		pass

for i in range(14216, 21576):
	try:
		words_ = (PlaintextCorpusReader(r'./nltk_data/corpora/reuters/test', str(i)).words())
		for j in words_:
			if j in orig.keys():
				j_list = orig[j]
				j_list.append(str(i))
				orig.update({j:list(set(j_list))})
			else:
				orig.update({j:[str(i)]})
	except ValueError:
		pass

# dict_ = {i:orig.count(i) for i in set(orig)}
dict_ = orig.copy()
for i in orig.keys():
	if i.isdigit() or (len(i) <= 1):
		dict_.pop(i)

sorted_dict = dict(sorted(dict_.items(), key = lambda k: k[0]))
sorted_dict_2 = {}
for i in sorted_dict.keys():
	if i.lower() not in sorted_dict_2.keys():
		sorted_dict_2.update({i.lower() : sorted_dict[i][:]})
	else:
		l = sorted_dict_2[i.lower()][:]
		l.extend(sorted_dict[i][:])
		sorted_dict_2[i.lower()] = l

del(sorted_dict)

with open("dictionary", "wb") as fp:   #Pickling
	dump(sorted_dict_2, fp, HIGHEST_PROTOCOL)

sorted_vocab = {i:len(sorted_dict_2[i]) for i in sorted_dict_2.keys()}

# sorted_vocab = dict(sorted(vocab.items(), key = lambda k: k[0]))

with open("vocabulary", "wb") as v:
	dump(sorted_vocab, v, HIGHEST_PROTOCOL)