import numpy as np
import random
from scipy import sparse as sp
from ClusterRoutines import *

ingredients_mat = np.loadtxt('Recipe_Ingredients.mtx')

# Try to find three different clusters for recipes (sweet, savory, drinks)

num_clusters = 3
num_recipes = ingredients_mat[0,0]
num_features = ingredients_mat[0,1]
num_rows = ingredients_mat.shape[0]

# convert the features matrix to csr format
data = ingredients_mat[1:num_rows+1, 2]
row_ind = ingredients_mat[1:num_rows+1, 0]
col_ind = ingredients_mat[1:num_rows+1, 1]
features = sp.coo_matrix((ingredients_mat[1:num_rows+1,2], (ingredients_mat[1:num_rows+1,0], ingredients_mat[1:num_rows+1,1])), shape=(num_recipes,num_features))
# convert features to dense matrix
features = features.todense()

# normalize features
mu = np.mean(features,axis=0)
norm_features = features - mu
stdev = np.std(norm_features, axis=0)
norm_features /= stdev

# Run the K-means algorithm to obtain clusters
max_iterations = 50
cluster_indices, centroids = runKMeans(max_iterations, num_clusters, norm_features)
print "centroids = ", centroids
print "cluster_indices = ", cluster_indices
