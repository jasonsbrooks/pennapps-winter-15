from flask import Flask
from bs4 import BeautifulSoup
import requests
import re
import gzip


URL = 'http://2015s.pennapps.com/'
FILENAME = 'temp.gzip'

def download(url, filename):
	response = requests.get(url)
	html_doc = response.text
	soup = BeautifulSoup(html_doc)

	#remove unnecessary
	elements = soup.findAll(['img', 'link', 'meta', 'style', 'script'])
	[element.extract() for element in elements]

	#remove attributes
	soup = removeAttrs(soup)

	for span in soup.findAll('span'):
	    span.parent.insert(span.parent.index(span)+1, span.text)
	    span.extract()


	#strip whitespace
	htmlString = unicode(soup).encode('utf-8')
	htmlString = removeWhitespace(htmlString)
	# f = open(filename, 'w')
	# f.write(htmlString)
	# f.close()
	compress(htmlString, filename)
	# print htmlString

def compress(string, filename):
	f = gzip.open(filename, 'wb')
	f.write(string)
	f.close()

def removeWhitespace(string):
	whitespace = ['\t', '\n', '\r']
	for character in whitespace:
		string = string.replace(character, '')

	return string

def removeAttrs(soup):
    for tag in soup.findAll(True): 
        tag.attrs = {}
    return soup

