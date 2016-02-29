import numpy as np
from ClusterRoutines import *

X = np.empty((100,2))
for i in xrange(50):
	X[i,0] = i
	X[i,1] = 0

for i in xrange(50,100):
	X[i,0] = 0
	X[i,1] = i-50

# shuffle the rows
np.random.shuffle(X)

# test to see if the find_closest_centroids algorithm works
num_centroids = 2
centroids = np.array([[25,0],[0,25]])
centroid_indices = find_closest_centroids(X, centroids)
# count total number of pts assigned to the two centroids respectively. 
# should be 50 each
num_assigned_to_first_centroid = len(np.where(centroid_indices == 0)[1])
num_assigned_to_second_centroid = len(np.where(centroid_indices == 1)[1])
print "number of points assigned to first centroid = ", num_assigned_to_first_centroid
print "number of points assigned to second centroid = ", num_assigned_to_second_centroid


# Now test to see if this centroid can be found using the K-means algorithm
num_clusters = 2
cluster_indices, centroids = runKMeans(50, num_clusters, X)

# Sometimes the code will be stuck at a local minimum
print "centroids = ", centroids
print "cluster_indices = ", cluster_indices
