# Class for Google Web Search Parsing
from bs4 import BeautifulSoup
from lib.connection import *
import urllib.request
import urllib.parse
import re


class GoogleSearch:
    headers =  {
        'User-Agent': 'Lynx/2.8.8dev.3 libwww-FM/2.14 SSL-MM/1.4.1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-us',
        'Accept-Encoding': 'identity',
        'Keep-Alive': '300',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
    }
    
    url = 'http://www.google.com/'
    query = 'q={0}&start={1}&num=100&complete=0'
    currentIndex = 100
    
    
    # Constructor: searchString is your query
    def __init__(self, searchString, debug=False):
            self.debug = False
            self.searchString = searchString
            self.html = ''
            self.requester = Requester("http://www.google.com/")
            for header, content in (self.headers.items()):
                self.requester.setHeader(header, content)
    

    # Public:
    def getFirstPageLinks(self):
        self.html = self.getHtml(0)
        links = self.parseLinks(self.html)

        return links
   

    def getNextPageLinks(self):
        self.initialize()
        self.html = self.getNextPage(self.html)
        links = self.parseLinks(self.html)

        return links
        
    def getPageLinksByPage(self, pageNumber):
        self.initialize()
        html = self.getHtml(0 * 100)
        links = self.parseLinks(html)
        return links
        
    def getCurrentPageNumber(self):
        self.initialize()
        result = getCurrentPageNumber(self.html)
        return result
        
    def getAproxResultsCount(self):
        self.initialize()
        result = self.getAproxResultsCount(self.html)
        return result
    
    # Private: 
    def initialize(self):
        if ((self.html == '') or (self.html == None)):
            self.html = self.getHtml(0)
    
    def getHtml(self, index):
        if self.debug:
            print('Starting request {0}'.format(requestUrl))
        result = self.requester.request("search", params = self.query.format(urllib.parse.quote(self.searchString), index * 100))
        if self.debug:
            print('Request Finished')
            
        return result.body
        
    def parseLinks(self, html):
        if not(html):
            return None
        soup = BeautifulSoup(html, "html.parser")
        links = (e['href'] for e in soup.findAll('a'))
        results = []
        regmatch = re.compile("^/url\?q=")
        for link in links:
            if None != regmatch.match(link):
                results.append(urllib.parse.unquote(link[7:link.find('&')]))
        return results
        
    def getAproxResultsCount(self, html):
        soup = BeautifulSoup(html)
        element = soup.find('div', attrs={'id' : 'resultStats'})
        #return element.text.split(' ')[2].replace(',', '')
        return element.text.replace(',', '')
        
    def getCurrentPageNumber(self, html):
        soup = BeautifulSoup(html, "html.parser")
        #print (soup.prettify())
        element = soup.find('font', attrs = {'size' : '-1', 'color' :'#a90a08'})
        if element:
            return int(element.text.encode()) - 1
        else:
            return 0
        
    def getNextPage(self, html):
        currPage = self.getCurrentPageNumber(html)
        soup = BeautifulSoup(html)

        # If no next Link, it's the last page
        img = soup.find('img', attrs = { 'src' : 'nav_next.gif' })
        
        if not(img):
            return None

        # Get the current page
        page = soup.find('font', attrs = {'size' : '-1', 'color' :'#a90a08'})
        result = self.getHtml(currPage + 1)

        return result