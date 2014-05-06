# Class for Bing API Parsing
from html.parser import HTMLParser
from bs4 import BeautifulSoup
from lib.connection import *
import urllib.request
import urllib.parse

class BingSearch:
	headers =  {
		'User-agent': 'Lynx/2.8.8dev.3 libwww-FM/2.14 SSL-MM/1.4.1',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Language': 'en-us',
		'Accept-Encoding': 'identity',
		'Cache-Control': 'max-age=0',
		'Cookie' : 'SRCHHPGUSR=NEWWND=1&NRSLT=50;FP=EM=23; _FS=NU=1; _SS=C=25.0&SID=9D7FD6370FDB4100803F5342F8A4B49F&CW=1264&CH=531&nhIm=19-; MUID=1E73174131C46FE90085149030D76FDB; SRCHD=SM=1&MS=2459777&D=2459777&AF=QBRE; SRCHUID=V=2&GUID=51642EBCB8AA409F814F393E4F84F4F2; SRCHUSR=AUTOREDIR=0&GEOVAR=&DOB=20120904; SCRHDN=ASD=0&DURL=#; _UR=TC=0; DUP=Q=j9tbve4hl0qQZ5_NJCLn&T=147592862&IG=90543ec28ebb461e8839f135c846d697&V=1&A=2; SRCHHPGUSR=NEWWND=1&NRSLT=50&SRCHLANG=&AS=0&ADLT=DEMOTE; _HOP=; RMS=F=OAAAAAAAAAR&A=AAAE; s_cc=true; s_vnum=1349323798881%26vn%3D1; s_nr=1346731798882; s_sq=%5B%5BB%5D%5D'
	}

	url = 'http://www.bing.com/'
	query = 'q={0}&first={1}&go=&qs=n&FORM=PORE'
	_currentIndex = 0

	# Constructor: searchString is your query
	def __init__(self, searchString, debug=False):
			self.debug = debug
			self.searchString = searchString
			self.html = ''
			self.requester = Requester(self.url)
			for header, content in (self.headers.items()):
				self.requester.setHeader(header, content)


	# Public
	def getFirstPageLinks(self):
		self._initialize()
		result =  self._parseLinks(self.html)
		return result

	def getNextPageLinks(self):
		if (self.html == "FINISHED"):
			return None
		newIndex = int(self._currentIndex + 1)
		html = self._getHtmlByPage(newIndex)
		links = self._parseLinks(html)
		if not(links):
			return None
		self.html = html
		self._currentIndex = newIndex
		s  = BeautifulSoup(self.html)
		if (self._getNextPageLink(self.html) == None):
			self.html = "FINISHED"
		return links
		

	# Private
	def _initialize(self):
		if ((self.html == '') or (self.html == None)):
			self.html = self._getHtmlByPage(0)
			self._currentIndex = 0

	def _getHtmlByPage(self, index):
		if self.debug:
			print('Starting request {0}'.format(requestUrl))
		result = self.requester.request("search", params = self.query.format(urllib.parse.quote(self.searchString), index * 100))
		if self.debug:
			print('Request Finished')

		return result.body
		
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