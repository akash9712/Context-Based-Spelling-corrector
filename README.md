# Context-Based-Spelling-corrector
A very basic context based spelling corrector built using the RCV1 dataset.
### Usage
Run top.py with Python 3 for demo.

### Key Assumptions
1) First alphabet of all the words in the query is correct (Common IR assumption)
2) Number and the order of words in the input query is correct.
3) There is no difference between Uppercase and Lowercase letters.

### Designed Model
Following steps are followed in the given order:  
Step 1 : Save the input query as a list using split function.  
Step 2 : Save the index of stopwords present in the query in the list non_corrections and
remove those stopwords.  
Step 3 : Make a list of lists pl[] which contains the posting lists of all the words present
in the query  
Step 4 : If the length of intersection of these posting lists is more than 4 then the query
has sufficient results and no correction is needed , else we find closewords using Damerau–
Levenshtein distance. *closewords is a 2-D python list, storing words with an edit distance
of less than 3 from the words in the original query.  
Step 5 : Replace one word at a time in the original query with each of its closewords
while keeping others the same , and if the length of posting list intersection decreases,
remove the closeword. Also remove all the stopwords suggested as closewords.  
Step 6 : For all the combinations of remaining closewords for which posting list inter-
section length > 4, add the stopwords which were previously removed and saved. These
combinations are now all the suggestions that will be displayed to the user.  
Step 7 : The suggestions generated in the previous step are shown in increasing order of
the expression :  
(edit _distance/word_similarity_count )
where the edit distance and the word_similarity_count is calculated between each
suggestion and the query.  
### Limitations
1) Since Reuters data is data primarily used for text classification, general web queries
are not relevant.
2) It is not a learning based model , therefore this model is not very user friendly.
Findings
1) Threshold for length of intersection of posting lists had to be kept low (4) for relevant
results to be displayed.
2) For finding list of closewords , modified edit distance approach works better than
Jaccard’s similarity index.
3) Using Damerau–Levenshtein i.e including swap as one of the operations with a lighter
weight than insert, delete ,replace operations gives better results.
4) The process of generating alternative spellings relevant to the original query is a two
tier process: First, we restrict our searches to only those with a significant number of
hits. Second, once we have narrowed down our suggestions, the frequency does not affect
the order in which the words are displayed. This is decided primarily using edit distance,
which leads to significantly better results.
