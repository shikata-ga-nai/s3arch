from lib.search.GoogleSearch import *
from lib.search.BingSearch import *
import urllib.parse


class Controller:
	def __init__(self, arguments):
		self.arguments = arguments
		if (self.arguments.query):
			self.searchQuery(arguments.query, arguments.google, arguments.bing)


	def searchQuery(self, query, google = True, bing = True):
		if (google == True):
			print("Searching in google")
			checked = []
			self.getResultsFromSearch(GoogleSearch(query), checked, printFound=True)
		if (bing == True):
			print("Searching in bing")
			checked = []
			self.getResultsFromSearch(BingSearch(query, False), checked, printFound=True)
			

	def getResultsFromSearch(self, search, checked, printFound=True):
		links = search.getFirstPageLinks()
		while(links != None):
			for l in links:			
				if (self.filterUrls(l, checked)):
					checked.append(l)
					if(printFound):
						print(l)
			links = search.getNextPageLinks()


	def filterUrls(self, url, checked):	
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
