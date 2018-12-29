from pickle import load

def intersect(x):
	"""Returns the intersection of a non negative number of lists."""
	final = x[0][:]
	for i in x[1:]:
		temp = [j for j in final if j in i]
		final = temp[:]
	return final

def load_vocab():
	"""Returns - dict: dict (word, no. of occurences)"""
	with open("vocabulary", "rb") as v:
		vocab = load(v)
	return vocab

def load_dictionary():
	"""Returns - dict: (word, posting list)"""
	with open("dictionary", "rb") as d:
		dict_ = load(d)
	return dict_

def load_bigrams():
	"""Returns - dict: (bigram, list of words containing the bigram)"""
	with open("bigrams", "rb") as b:
		bg = load(b)
	return bg

def get_category_dict():
	"""Returns the list of categories for doc_id in Reuters"""
	with open("categories", "rb") as c:
		cat = load(c)
	return cat

def get_inv_category_dict():
	"""Returns the list of categories for doc_id in Reuters"""
	with open("inverted_categ_dict", "rb") as c:
		cat = load(c)
	return cat


def combos(l):
	"""
	l: list of lists, with each inner list consisting of strings
	=======
	Returns all combinations of the strings in the inner list.
	"""
	if(len(l) == 1):
		return l[0]
	s = []
	for i in range(len(l[0])):
		k = combos(l[1:])
		for j in range(len(k)):
			s.append(l[0][i] + " " + k[j])
	return s

def edit_distance(word1, word2):
	from numpy import zeros
	swap_cost = 0.5 # cost for the rest = 1 
	word1l = list(word1)
	word2l = list(word2)
	if(len(word1l) == 0):
		return len(word2l)
	elif(len(word2l) == 0):
		return len(word2l)
		 
	a = zeros((len(word1l) + 1, len(word2l) + 1))
	for i in range(0, len(word1l) + 1):
		for j in range(0, len(word2l) + 1):
			if(i == 0):
				a[i][j] = j
			elif(j == 0):
				a[i][j] = i
			elif(word1l[i - 1] == word2l[j - 1]):
				a[i][j] = a[i - 1][j - 1]
			else:
				a[i][j] = 1 + min(a[i - 1][j], a[i][j - 1], a[i - 1][j - 1])

			if(i > 1 and j > 1 and word1l[i - 1] == word2[j - 2] and\
				word1l[i - 2] == word2l[j - 1]):

				a[i][j] = min(a[i][j], a[i - 2][j - 2] +swap_cost)
	# for i in range(len(a)):
	# 	print(a[i])
	return a[len(word1l)][len(word2l)]

def split_k_grams(k, word):
	rv = []
	for i in range(len(word) - k + 1):
		kg = word[i:i+k]
		rv.append(kg)
	rv.append(word[len(word) + 1 - k:] + '$')
	return rv

def jaccard_similarity(word1, word2):
	l1 = split_k_grams(2, word1)
	l2 = split_k_grams(2, word2)
	return len(intersect([l1, l2]))/(len(l1) + len(l2) - len(intersect([l1, l2])))
	
def category_index():
	"""
	Return a dictionary with keys as categories and values as a list of 
	files belonging to the category.
	"""
	from nltk.corpus import reuters
	known = reuters.categories()
	rv = {} 
	for i in range(21576):
		categs = get_category(i)
		for j in categs:
			if j not in known:
				print("New category.")
			if j in rv.keys():
				rv[j].extend([i])
			else:
				rv.update({j:[i]})
	return rv

def categ_count():
	"""
	Return a dictionary with keys as categories and values as the no. of files
	belonging to the category, with keys sorted in decending order of their 
	frequencies.
	"""
	d = category_index()
	sorted_d = {}
	for i in d.keys():
		sorted_d.update({i: len(d[i])})
	sorted_d = dict(sorted(sorted_d.items(), key = lambda k: -k[1]))
	return sorted_d