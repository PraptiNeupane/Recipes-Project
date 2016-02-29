import numpy as np
import random
from scipy import sparse as sp
from clusterRoutines import *

ingredients_mat = np.loadtxt('Recipe_Ingredients.mtx')

# Try to find three different clusters for recipes (sweet, savory, drinks)

num_clusters = 2
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


# initialize cluster centers
centroids = initialize_centroids(num_clusters, features)

# find initial clusters
cluster_indices = find_closest_centroids(features, centroids)
centroids = compute_centroids(features, cluster_indices, num_clusters)

print "centroids = ", centroids
