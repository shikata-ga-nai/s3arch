# Class for Bing API Parsing
from thirdparty.BeautifulSoup import BeautifulSoup
import urllib.request
import urllib.parse

class BingSearch:
	headers =  {
		'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:11.0) Gecko/20100101 Firefox/11.0',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Language': 'en-us',
		'Accept-Encoding': 'identity',
		'Keep-Alive': '300',
		'Connection': 'keep-alive',
		'Cache-Control': 'max-age=0',
		'Cookie' : 'SRCHHPGUSR=NEWWND=1&NRSLT=50;FP=EM=23; _FS=NU=1; _SS=C=25.0&SID=9D7FD6370FDB4100803F5342F8A4B49F&CW=1264&CH=531&nhIm=19-; MUID=1E73174131C46FE90085149030D76FDB; SRCHD=SM=1&MS=2459777&D=2459777&AF=QBRE; SRCHUID=V=2&GUID=51642EBCB8AA409F814F393E4F84F4F2; SRCHUSR=AUTOREDIR=0&GEOVAR=&DOB=20120904; SCRHDN=ASD=0&DURL=#; _UR=TC=0; DUP=Q=j9tbve4hl0qQZ5_NJCLn&T=147592862&IG=90543ec28ebb461e8839f135c846d697&V=1&A=2; SRCHHPGUSR=NEWWND=1&NRSLT=50&SRCHLANG=&AS=0&ADLT=DEMOTE; _HOP=; RMS=F=OAAAAAAAAAR&A=AAAE; s_cc=true; s_vnum=1349323798881%26vn%3D1; s_nr=1346731798882; s_sq=%5B%5BB%5D%5D'
	}

	url = 'http://www.bing.com/search?q={0}&first={1}&go=&qs=n&FORM=PORE'
	_currentIndex = 0

	# Constructor: searchString is your query
	def __init__(self, searchString, debug=False):
			self.debug = debug
			self._searchString = searchString
			self._html = ''
	# Public
	def getFirstPageLinks(self):
		self._initialize()
		result =  self._parseLinks(self._html)
		return result

	def getNextPageLinks(self):
		if (self._html == "FINISHED"):
			return None
		newIndex = int(self._currentIndex + 1)
		html = self._getHtmlByPage(newIndex)
		links = self._parseLinks(html)
		if not(links):
			print ("NONE")
			return None
		self._html = html
		self._currentIndex = newIndex
		s  = BeautifulSoup(self._html)
		if (self._getNextPageLink(self._html) == None):
			self._html = "FINISHED"
		return links
		

	# Private
	def _initialize(self):
		if ((self._html == '') or (self._html == None)):
			self._html = self._getHtmlByPage(0)
			self._currentIndex = 0

	def _getHtmlByPage(self, index):
		opener = urllib.request.build_opener()
		requestUrl = self.url.format(urllib.parse.quote(self._searchString), (1 + (int(index) * 50)))
		if self.debug:
			print('Starting request {0}'.format(requestUrl))
		request = urllib.request.Request(requestUrl, None, self.headers)
		result = opener.open(request).read().decode()
		if self.debug:
			print('Request Finished')
		return result
		
	def _parseLinks(self, html):
		if not(html):
			return None
		soup = BeautifulSoup(html)
		links = (e.find('a')['href'] for e in soup.findAll('div', attrs={'class' : 'sb_tlst'}))
		return links

	def _getNextPageLink(self, html):
		#currPage = self.getCurrentPageNumber(html)
		soup = BeautifulSoup(html)
		element = soup.find('a', attrs={'class' : 'sb_pagN'})
		if not(element):
			return None
		nextPageUrl = 'http://www.bing.com/{0}'.format(element['href'])
		return nextPageUrl