import numpy as np
import random 
import scipy

r""" This function initializes the centroids for the clusters by randomly picking
		 num_clusters number of entries from the features matrix"""
def initialize_centroids(num_clusters, features):
	(num_recipes, num_features) = features.shape
	centroid_index = [random.randrange(0,num_recipes,1) for i in xrange(num_clusters)]
	centroids = np.zeros((num_clusters, num_features))
	for i in xrange(num_clusters):
		index = centroid_index[i]
		centroids[i,:] = features[index,:]
	return centroids


r""" This function stores the index of the closest centroid in the cluster_index array 
		for each of the data points"""
def find_closest_centroids(features, centroids):
	(num_centroids, num_features) = centroids.shape
	(num_points, num_features) = features.shape
	cluster_indices = np.empty((1,num_points))
	for i in xrange(num_points):
		curr_vec_mat = np.array(np.tile(features[i,:], (num_centroids,1)))
		distance_mat = curr_vec_mat - centroids
		sq_distance = distance_mat*distance_mat
		distance_vec = np.sum(distance_mat*distance_mat, axis=1)
		cluster_indices[0,i] = distance_vec.argmin()

	return cluster_indices


r""" This function calculates the centroid of each cluster """
def compute_centroids(features, cluster_indices, num_clusters):
	(num_pts, num_features) = features.shape
	centroids = np.empty((num_clusters, num_features))
	for i in xrange(num_clusters):
		(dummy, pt_indices) = np.where(cluster_indices == i)
		my_cluster = features[pt_indices, :]
		centroids[i,:] = np.mean(my_cluster, axis=0)
	
	return centroids

def runKMeans(max_iterations, num_clusters, features):
	# initialize cluster centers
	centroids = initialize_centroids(num_clusters, features)
	
	# iterate between finding centroids and assigning points to clusters
	for i in xrange(max_iterations):
		print "K-Means iteration ", i, " in progress ......"
		# assign each point to a cluster
		cluster_indices = find_closest_centroids(features, centroids)
		# calculate new centroids
		centroids = compute_centroids(features, cluster_indices, num_clusters)

	return cluster_indices, centroids

