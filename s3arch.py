#!/usr/bin/env python3
from GoogleSearch import GoogleSearch
from BingSearch import BingSearch
import urllib.parse
import sys

def filterUrls(url, checked):	
	if (url.find('?') == -1):
		return False
	parsed = urllib.parse.urlparse(url)
	params = (t.split('=', 1) for t in parsed.query.split('&'))
	try:
		params = '&'.join(a + '=' for a, b in params)
	except ValueError:
		return False
	url = parsed.scheme + parsed.netloc + parsed.path + '?' + params
	if (checked.count(url) == 0):
		checked.append(url)
		return True
	else:
		return False
		

def SearchInGooge(query, checked, printFound=True):
	g = GoogleSearch(query)
	links = g.getFirstPageLinks()
	while(links != None):
		for l in links:		
		
			if (filterUrls(l, checked)):
				checked.append(l)
				if(printFound):
					print(l)
			#else:
			#	print(l)
		links = g.getNextPageLinks()

def SearchInBing(query, checked, printFound=True):
	b = BingSearch(query, False)
	links  = b.getFirstPageLinks()
	while(links != None):
		for l in links:
			if (filterUrls(l, checked)):
				checked.append(l)
				if(printFound):
					print(l)
			#else:
			#	print(l)
		links = b.getNextPageLinks()

def main():
	print("s3arch v0.1")
	query = sys.argv[1]
	checked = []
	dynamicContent = [
		'','php','php4','php5','asp','aspx','ashx','axd','jsp','do',
		'html','shtml','htm','pl','cgi','xml'
		]
	staticContent = ['conf','log','swf','sql','rdp','xml','txt']
	print("+ - Searching in GOOGLE engine")
	SearchInGooge(query, checked, True)
	print("+ - Searching in BING engine")
	SearchInBing(query, checked, True)
	print ("---END---")

	
	
if __name__ == '__main__':
	main()
	