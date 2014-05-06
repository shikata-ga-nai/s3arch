from lib.connection import *
import urllib.request
import urllib.parse
import re


class BaseSearch(Object):
    headers =  {
        'User-agent': 'Lynx/2.8.8dev.3 libwww-FM/2.14 SSL-MM/1.4.1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-us',
        'Accept-Encoding': 'identity',
        'Cache-Control': 'max-age=0',
        'Cookie' : ''
    }

    def __init__(self, searchString):
        self.searchString = searchString
        self.html = ''
        self.requester = Requester(self.getUrl())
        for header, content in (self.headers.items()):
            self.requester.setHeader(header, content)


    def initialize(self):
        if ((self.html == '') or (self.html == None)):
            self.html = self.getHtml(0)


    def getFirstPageResults(self):
        self.html = self.getHtml(0)
        links = self.parseResults(self.html)

        return links
   

    def getNextPageResults(self):
        self.initialize()
        self.html = self.getNextPage(self.html)
        links = self.parseResults(self.html)

        return links


    def getHtml(self, index):
        result = self.requester.request(self.getPath(), \
            params = self.query.format(self.getQuottedSearchString, \
                self.getFormattedIndex(index)))
        if self.debug:
            print('Request Finished')
            
        return result.body


    def getQuottedSearchString(self):
        return urllib.parse.quote(self.searchString)


    def getFormattedIndex(self, index):
        return index * 100


#Abstract Methods

    @abstractmethod
    def parseResults(self, html): raise NotImplementedError


    @abstractmethod
    def getNextPage(self, html): raise NotImplementedError


    @abstractmethod
    def getAproxResultsCount(self, html): raise NotImplementedError


    @abstractmethod
    def getUrl(self): raise NotImplementedError


    @abstractmethod
    def getPath(self): raise NotImplementedError


    @abstractmethod
    def getParameters(self): raise NotImplementedError


    @abstractmethod
    def getCurrentPageNumber(self): raise NotImplementedError

