r"This file downloads the recipes from gourmetsleuth.com"

import urllib
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from fractions import Fraction

# this function converts every measure to tbsp
def convert_units_to_tbsp(measure, amount, ingredient,recipe_name):
	#print "recipe_name = ", recipe_name,  "measure = ", measure, " amount = ", amount, " ingredient = ", ingredient
	new_amount = amount.replace('//', '/')
	if new_amount:
		amount = new_amount

	new_amount = amount.replace('-', ' ' )
	if new_amount:
		amount = new_amount

	new_amount = amount.replace(' / ', '/')
	if new_amount:
		amount = new_amount

	if amount == 'NA':
		amount = 1.0
	else:
		try:
			amount = float(sum(Fraction(s) for s in amount.split()))
		except ValueError:
			try:
				amount = float(sum(Fraction(s) for s in amount.replace('/', '').split()))
			# just use a value that won't have much weight
			except ValueError:
				amount = 0.01

			
	if (measure == 'cups' or measure == 'cup'):
		return 16*amount
	elif (measure == 'tbsp' or measure == 'tablespoon' or measure == 'tablespoons' or measure == 'tbsps' or measure == 'TB' or measure == 'T' or measure == 'Tbl'):
		return amount
	elif (measure == 'tsp' or measure == 'tsps' or measure == 'teaspoon' or measure == 'teaspoons' or measure == 't'):
		return amount/3.0
	# just assume that for now, a pound of anything is 2 cups
	elif (measure == 'pound' or measure == 'pounds' or measure == 'Lb' or measure == 'Lbs'):
		return amount*2*16
	# assume its fluid ounces
	elif (measure == 'ounces' or measure == 'ounce' or measure == 'oz' or measure == 'ozs'):
		return amount*2
	elif (measure == 'pinch'):
		return 0.1
	# for everything else return just the amount
	else:
		return amount


ingredients_array = []
recipes_names = []
recipes_ingredients = []
recipes_amount = []
recipes_measures = []
recipes_instructions = []

recipes_df = pd.DataFrame(columns = ('Name', 'Ingredients', 'Instructions'))

root_url = 'http://www.gourmetsleuth.com'
recipes_url = root_url+'/recipes'

courses_list = []
courses_url = []

# Obtain different courses
recipes_html = urllib.urlopen(recipes_url).read()
soup = BeautifulSoup(recipes_html, 'html.parser')
categories = soup.find_all('li', attrs={"class": "sftaxonItem"})

for tag in categories:
	h3_class = tag.find('h3', attrs = {"class": "root-taxon"})
	if h3_class:
		if (h3_class.contents[0] == 'Course'):
			Courses = tag.find_all('li', attrs = {"class": "sftaxonItem accent-dash-1px"})
			for course in Courses:
				tags = course.find('a')
				course_name = tags.contents[0]
				course_ref = tags.get('href', None)
				if course_ref:
					courses_list.append(course_name.encode('ascii','ignore').lower())
					courses_url.append(root_url+course_ref)

# Download recipes by courses
course_num = 0
recipe_num = 0
for course in courses_list:
	course_url = courses_url[course_num]
	print "course_url = ", course_url
	course_html = urllib.urlopen(course_url).read()
	my_soup = BeautifulSoup(course_html, 'html.parser')
# browse dishes by clicking on the view all link
	view_all = my_soup.find('a', id="cph_content_C016_ctl00_ctl00_viewAllLink") 
	view_all_link = root_url+ view_all.get('href', None)
	all_dishes_html = urllib.urlopen(view_all_link).read()
	all_soup = BeautifulSoup(all_dishes_html, 'html.parser')

	pages_links_list = all_soup.find('div', attrs = {"id":"cph_content_C016_ctl00_ctl00_viewAllPager_ctl00_ctl00_numeric"})
	pages_links = pages_links_list.find_all('a')

# loop over all the pages for that category
	for page in pages_links:
		page_link = root_url+page.get('href', None)
		page_html = urllib.urlopen(page_link).read()
		page_soup = BeautifulSoup(page_html, 'html.parser')
		food_items = page_soup.find_all('div', attrs={"class":"simple-image-wrapper"})

		# 	loop over all the items on that page
		for item in food_items:
			# create a dictionary to hold the recipe information about this food item
			#recipe_dict = { }
			recipe_url = root_url + item.find('a').get('href')
			recipe_name = item.find('span').contents[0]

			try:
				recipe_html = urllib.urlopen(recipe_url)
			except:
				continue

			#print "recipe = ", recipe_url
			recipe_soup = BeautifulSoup(recipe_html, 'html.parser')

			# Make a list of all the ingredients needed for this recipe
			ingredients_string = ''
			ingredients = recipe_soup.find_all('li', itemprop="ingredients")
			curr_ingredients = list()
			curr_amount = list()
			curr_measure = list()
			for ingredient_details in ingredients:
				try:
					amount = ingredient_details.find('span', attrs={"class":"amount"}).contents[0]
					curr_amount.append(amount)
				except IndexError:
					amount = ' '
					curr_amount.append('NA')
				try:
					measure = ingredient_details.find('span', attrs = {"class":"measure"}).contents[0]
					curr_measure.append(measure)
				except IndexError:
					measure = ' '
					curr_measure.append('NA')

				ingredient = ingredient_details.find('span', attrs={"class":"ingredient"})
				
				#print "ingredient_details = ", ingredient_details
				#print "ingredient = ", ingredient
				try:
					ingredient = ingredient.find('a').contents[0]
					curr_ingredients.append(ingredient)
				except AttributeError:
					if len(ingredient.contents) > 0:
						ingredient = ingredient.contents[0]
						curr_ingredients.append(ingredient)
					else:
						ingredient = ''
						curr_ingredients.append('NA')
					
			my_ingredients_array = np.zeros(len(ingredients_array))
			for item in curr_ingredients:
				if item not in ingredients_array:
					ingredients_array.append(item)

			recipes_names.append(recipe_name.encode('ascii','ignore'))
			recipes_ingredients.append(curr_ingredients)
			recipes_amount.append(curr_amount)
			recipes_measures.append(curr_measure)
			
			# Now find instructions
			instructions = recipe_soup.find('div', itemprop='recipeInstructions')
			if instructions:
				instructions = instructions.get_text()
			else:
				instructions = ''

			recipes_instructions.append(instructions)
			
#			recipe_df = pd.DataFrame(data=recipe_dict, index = [recipe_num])
#			recipes_df = pd.concat([recipes_df,recipe_df])
			recipe_num += 1
		break
	
	break

	course_num += 1

# now for each recipe, create an ingredient list that is as long as ingredients_array
num_ingredients = len(ingredients_array)
print "total ingredients = ", num_ingredients
recipe_ingredients_large_array = []
num_recipes = len(recipes_names)
for i in xrange(num_recipes):
	curr_ing_array = np.zeros(num_ingredients)
	ingredients = recipes_ingredients[i]
	amounts = recipes_amount[i]
	measures = recipes_measures[i]
	num_ings = len(ingredients)
	for j in xrange(num_ings):
		curr_ing = ingredients[j]
		curr_measure = measures[j]
		curr_amount = amounts[j]
		index = ingredients_array.index(curr_ing)
		curr_ing_array[index] = convert_units_to_tbsp(curr_measure, curr_amount, curr_ing, recipes_names[i])

	recipe_ingredients_large_array.append(curr_ing_array)

np_recipe_names = np.array(recipes_names)
np_recipe_ingredients = np.array(recipe_ingredients_large_array)
np_recipe_instructions = np.array(recipes_instructions)


nameFile = open('./Recipe_Names.txt', 'w')
for item in recipes_names:
	  nameFile.write("%s\n" % item)
nameFile.close()

np.savetxt('./Recipe_Ingredients.txt', np_recipe_ingredients)

#instFile = open('./Recipe_Instructions.txt', 'w')
#instFile.write("Recipe 0 \n")
#itemnum = 0
#for item in recipes_instructions:
#	instFile.write("{}\n".format(item.encode('ascii','ignore')))
#	instFile.write("Recipe {}\n".format(itemnum))
#	itemnum += 1
#instFile.close()

	

#recipes_df.to_pickle('Recipes_DataFrame.pkl')
#print "recipes_df = " , recipes_df
