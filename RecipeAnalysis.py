import pandas as pd
import nltk
import string
from scipy import argwhere

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import pairwise_distances
from nltk.stem.porter import PorterStemmer


stemmer = PorterStemmer()
def tokenize(text):
	tokens = nltk.word_tokenize(text)
	stems = []
	for token in tokens:
		stems.append(stemmer.stem(token))
	return stems

RD = pd.read_pickle('./Recipes_DataFrame.pkl')
Recipes_Names = RD['Name'].as_matrix()

# convert strings and instructions to lower case
RD['Ingredients and Instructions'] = RD['Ingredients and Instructions'].apply(lambda row: row.lower())

# remove the punctuation using the character deletion step of translate
RD['Ingredients and Instructions'] = RD['Ingredients and Instructions'].apply(lambda row: row.translate(None, string.punctuation))

# calculate tf-idf
tfidf = TfidfVectorizer(tokenizer=tokenize, stop_words='english')
tfidf_mat = tfidf.fit_transform(RD['Ingredients and Instructions'])

# Calculate the cosine similarity between two recipes as a sanity check
cosine_similarity = pairwise_distances(tfidf_mat, metric='cosine')
distances = 1-cosine_similarity

cheeseballs_ind = argwhere(Recipes_Names == 'Bacon Cheese Puff Balls')[0][0]
flan_ind = argwhere(Recipes_Names == 'Mexican Flan')[0][0]
brussels_ind = argwhere(Recipes_Names == 'Buffalo Brussels Sprouts')[0][0]
key_lime_bars_ind = argwhere(Recipes_Names == 'Key Lime Bars')[0][0]
key_lime_cookies_ind = argwhere(Recipes_Names == 'Key Lime Cookies')[0][0]
margarita_ind = argwhere(Recipes_Names == 'Cranberry Margarita')[0][0]
print "similarity between bacon puff cheese balls and flan = ", distances[cheeseballs_ind, flan_ind]
print "similarity between bacon puff cheese balls and buffalo brussels sprouts = ", distances[cheeseballs_ind, brussels_ind]
print "similary between key lime bars and key lime cookies = ", distances[key_lime_bars_ind, key_lime_cookies_ind]
print "similarity between key lime bars and cranberry margarita = ", distances[key_lime_bars_ind, margarita_ind]

# Now find 5 Nearest Neighbors
from sklearn.neighbors import NearestNeighbors
neigh = NearestNeighbors(n_neighbors=5, algorithm='auto')
neigh.fit(tfidf_mat)
# print out the nearest neighbors for a few items
nearest_neighbors = neigh.kneighbors(return_distance= False)

query_names = ['Bacon Cheese Puff Balls', 'Mexican Flan', 'Buffalo Brussels Sprouts', 'Key Lime Bars', 'Key Lime Cookies', 'Cranberry Margarita']
query_inds = [cheeseballs_ind, flan_ind, brussels_ind, key_lime_bars_ind, key_lime_cookies_ind, margarita_ind]

j = 0
for recipe in query_names:
	query_ind = argwhere(Recipes_Names == recipe)[0][0]
	print "The five recipes closest to ", recipe, " are:"
 	for i in xrange(5):
		curr_ind = nearest_neighbors[query_ind][i]
		next_ind = curr_ind+1
		print Recipes_Names[curr_ind]
	j += 1

