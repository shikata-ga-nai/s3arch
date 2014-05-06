from lib.search.GoogleSearch import *
from lib.search.BingSearch import *
import urllib.parse

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