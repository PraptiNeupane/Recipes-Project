r""" This file downloads all the ingredients listed in gourmetsleuth.com 
	 Then it writes the ingredients to the file Ingredients.txt """ 

import urllib
from bs4 import BeautifulSoup
import string

root_url = 'http://www.gourmetsleuth.com'
ingredients_url = root_url+'/ingredients'

ingredients_list = []
for letter in list(string.ascii_lowercase):
#for letter in ['a','b','c']:
	ingredients_child_url = ingredients_url+'/'+letter
	ingredients_html = urllib.urlopen(ingredients_child_url).read()
	soup = BeautifulSoup(ingredients_html, 'html.parser')
	pages_lists = soup.find_all('ul', attrs={"class": "sf_pagerNumeric"})
	for l in pages_lists:
		pages_links = l.find_all('a')
		for link in pages_links:
			page_url = link.get('href',None)
			page_url = root_url+page_url
			page_html = urllib.urlopen(page_url).read()
			next_soup = BeautifulSoup(page_html, 'html.parser')
			letter_ingredients = next_soup.find_all('div', attrs={"class": "portfolio_dscr"})
			for tag in letter_ingredients:
				ingredients_list.append(tag.a.contents[0].encode('ascii','ignore').lower())

f = open('Ingredients.txt', 'w')
for item in ingredients_list:
	f.write("{}\n".format(item))
f.close()
