import numpy as np
from scipy import sparse as sp
from sklearn.cluster import KMeans
from sklearn.preprocessing import scale

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
features = features.todense()

# normalize features
features = scale(features)
kmeans = KMeans(init='random', n_clusters=num_clusters, n_init=10)
cluster_indices = kmeans.fit_predict(features)

print "cluster_indices = ", cluster_indices


