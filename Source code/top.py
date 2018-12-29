from utilities import *
from pickle import load
from collections import OrderedDict
from nltk.corpus import PlaintextCorpusReader

stopwords = PlaintextCorpusReader(r'./nltk_data/corpora/reuters', 'stopwords').words()

print("Enter Query:")

query = input().split()

non_corrections = {}
for i in range(len(query)):
	if(len(query[i]) == 1 or query[i] in stopwords):
		non_corrections.update({query[i] : i})

# print(non_corrections)

for i in query[:]:
	if(len(i) == 1 or i in stopwords):
		query.remove(i)

for i in range(len(query)):
	query[i] = query[i].lower()

d = load_dictionary().copy()

flag = 0
pl = []
for i in query:
	try:
		pl.append(d[i])
	except KeyError:
		flag = 1

# print("No. of hits: " + str(len(intersect(pl))))
if(len(pl) > 0):
	if(len(intersect(pl)) > 4 and (not flag)): # The query has sufficient results, no correction needed.
		print("Valid query.")
		exit()
# print("test")
if(flag == 1):
	pl = []

####################################
# Spelling correction begins here. #
####################################

# bigrams = load_bigrams()
close_words = []

vocab = load_vocab()

for i in query:
	bg = []
	for j in list(filter(lambda x: x[0] == i[0], vocab.keys())):#split_k_grams(2, i):
		# for k in bigrams[j]:
		# 	if(jaccard_similarity(i, k) > 0.5):
		if(edit_distance(i, j) <= 2):
				bg.append(j)
	close_words.append(list(set(bg)))
	# For index I, close_words[I] corresponds to words containing all 
	# bigrams of query[I] with jaccard index higher than set threshold.

# alt_queries = combos(close_words)

alt_queries = []
for i in range(len(query)):
	q_copy = query[:]
	# print(i)
	for j in close_words[i]:
		q_copy[i] = j
		pl_ = []
		for k in q_copy:
			try:
				pl_.append(d[k])
			except KeyError:
				continue
		if((len(pl_) > 0 and len(pl) > 0) and\
		 (len(intersect(pl_)) < len(intersect(pl)))):
			close_words[i].remove(j)
		elif(j in stopwords):
			close_words[i].remove(j)
	# print(close_words)
# exit()
alt_queries = combos(close_words)
suggestions = {}
for q in alt_queries:
	pl2 = []
	flag = 0
	for i in q.split():
		try:
			pl2.append(d[i])
		except KeyError:
			flag = 1
			break
	if(len(intersect(pl2)) > 4 and (not flag)):
		suggestions.update({q : (len(intersect(pl2)))})

suggestions = OrderedDict(sorted(suggestions.items(), key = lambda x: sum(
	[edit_distance(x[0].split()[i], query[i]) for i in range(len(query))])))
# print(suggestions)

for i in suggestions:
	spl = i.split()
	suggestions[i] = sum([edit_distance(spl[q], query[q]) for q in range(len(spl))]) 
	


suggestions_ = OrderedDict()
for i in suggestions:
	l = i.split()
	for j in non_corrections:
		l.insert(non_corrections[j], j)
		# print(l)
	suggestions_.update({' '.join(l) : suggestions[i]})

# print(suggestions)
# exit()
from nltk.corpus import wordnet 

# Calculate the 
word_similaritiy_count = OrderedDict((i, None) for i in suggestions_)
for i in word_similaritiy_count:
	flag = False
	l = i.split(); l1 = l.copy()
	for s in l1:
		if s in stopwords:
			l.remove(s)
	mean = []
	int_l = 1
	if(len(l) <= 1):
		word_similaritiy_count[i] = 1
		continue
	else:
		for j in l:
			try:
				m = wordnet.synsets(j)[0].definition().split()
			except IndexError:
				word_similaritiy_count[i] = 1
				flag = True
			for y in m[:]:
				if y in stopwords:
					m.remove(y)
			mean.append(m)
		if(not flag):
			int_l += len(intersect(mean))
			word_similaritiy_count[i] = int_l



suggestions_final = OrderedDict((i,
	 suggestions_[i]/word_similaritiy_count[i]) for i in suggestions_)

suggestions_final = OrderedDict(sorted(suggestions_final.items(), key = lambda x: x[1]))


BOLD = '\033[1m'
END = '\033[0m'
if(len(suggestions_final) == 0):
	print("Sorry, no relevant alternatives were found to your query.")
	exit()
print("Did you mean any of the following?")
# limit = 0
for i in suggestions_final:
	# limit+=1
	print(BOLD + str(i) + " : " + str(suggestions_final[i]) + END)
