from lib.core.Url import *
from lib.search.GoogleSearch import *
from lib.search.BingSearch import *
from queue import Queue as queue



class Controller:
    def __init__(self, arguments):
        self.arguments = arguments
        self.checked = []
        self.recursiveQueue = queue()
        self.recursiveList = []
        if (self.arguments.query):
            self.searchQuery(arguments.query, arguments.google, arguments.bing)
        if (self.arguments.site):
            self.recursiveQueue.put(arguments.site)
            while not self.recursiveQueue.empty():
                site = self.recursiveQueue.get()
                #print("Searching in {0}".format(site))
                query = "site:{0}".format(site)
                if self.arguments.custom:
                    query += " " + self.arguments.custom
                self.searchQuery(query, arguments.google, arguments.bing)




    def searchQuery(self, query, google = True, bing = True):
        
        if (google == True):
            print("Searching in google")
            for url in self.getResultsFromSearch(GoogleSearch(query)):
                self.addDirectory(url)
                if self.filter(url): print(url)
        if (bing == True):
            print("Searching in bing")
            for url in  self.getResultsFromSearch(BingSearch(query, False)):
                self.addDirectory(url)
                if self.filter(url): print(url)

            

    def getResultsFromSearch(self, search):
        links = search.getFirstPageLinks()
        while links:
            for l in links:         
                yield Url(l)
            links = search.getNextPageLinks()


    def filter(self, url):
        if self.arguments.parameters and not url.hasParameters():
            return False
        if self.arguments.numeric and not url.hasIntegerValue():
            return False
        if url.getWithoutParamValues() in self.checked:
            return False
        else:
            self.checked.append(url.getWithoutParamValues())
        return True

    def addDirectory(self, url):
        if not self.arguments.recursive: return
        if url.getDirectory() not in self.recursiveList:
            self.recursiveQueue.put(url.getDirectory())
            self.recursiveList.append(url.getDirectory())
    