This project aims to collect a database of different recipes and use some machine learning algorithms to find similar recipes with the ultimate goal of being able to suggest recipes based on similarity to other recipes or ingredients at hand. The current status of the project is described below:

Current status of project:
	- An initial small database of recipes is created by downloading recipes from the website "GourmetSleuth.com"
	- The code used to crawl the website is included in this repo
	- Need a better way of handling recipe entries with no ingredients or instructions. Currently, such entry (like mojito of the future) shows up as the closest recipe to every recipe while using the k nearest neighbor algorithm
	- While converting the features matrix to csr_array, nnz decreases, which seems to imply that there are some repetitions of row and column indices when the features matrix is being created
	- Haven't implemented a way to get the solution out of a local minimum. Need to implement a function that will run kmeans multiple times, and picks the solution with the lowest "cost" associated with it
	- Checked the solution against the one produced by using the scikit learn function. The solution is the same
	- Checked to see if the matrix obtained using tfidf will work as a better indicator of features of the recipe in file "RecipeAnalysis.py". But still obtain the same solution
	- Conclusion: Maybe not the best dataset for unsupervised learning. Try classification next.

