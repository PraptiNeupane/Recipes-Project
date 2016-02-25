r"This file downloads the recipes from gourmetsleuth.com"

import urllib
from bs4 import BeautifulSoup
import pandas as pd

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
			recipe_dict = { }
			recipe_url = root_url + item.find('a').get('href')
			recipe_name = item.find('span').contents[0]
			recipe_dict['Name'] = recipe_name

			try:
				recipe_html = urllib.urlopen(recipe_url)
			except:
				continue

			print "recipe = ", recipe_url
			recipe_soup = BeautifulSoup(recipe_html, 'html.parser')

			# Make a list of all the ingredients needed for this recipe
			ingredients_string = ''
			ingredients = recipe_soup.find_all('li', itemprop="ingredients")
			for ingredient_details in ingredients:
				try:
					amount = ingredient_details.find('span', attrs={"class":"amount"}).contents[0]
				except IndexError:
					amount = ' '
				try:
					measure = ingredient_details.find('span', attrs = {"class":"measure"}).contents[0]
				except IndexError:
					measure = ' '

				ingredient = ingredient_details.find('span', attrs={"class":"ingredient"})
				
				#print "ingredient_details = ", ingredient_details
				#print "ingredient = ", ingredient
				try:
					ingredient = ingredient.find('a').contents[0]
				except AttributeError:
					if len(ingredient.contents) > 0:
						ingredient = ingredient.contents[0]
					else:
						ingredient = ''
				
				ingredients_string += amount + ' ' +  measure + ' ' + ingredient + '\n '

			recipe_dict['Ingredients'] = ingredients_string
			# Now find instructions
			instructions = recipe_soup.find('div', itemprop='recipeInstructions')
			if instructions:
				instructions = instructions.get_text()
			else:
				instructions = ''
			recipe_dict['Instructions'] = instructions

			
			recipe_df = pd.DataFrame(data=recipe_dict, index = [recipe_num])
			recipes_df = pd.concat([recipes_df,recipe_df])
			recipe_num += 1
			
	course_num += 1

recipes_df.to_pickle('Recipes_DataFrame.pkl')
print "recipes_df = " , recipes_df
