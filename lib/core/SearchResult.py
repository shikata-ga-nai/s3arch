from .Url import *

class SearchResult:
    def __init__(self, url=None, title=None, description=None, date=None):
        self.url = Url(url)
        self.title = title
        self.description = description
        self.date = date

    def __str__(self):
        return self.url

    def __cmp__(self, other):
        return cmp(self.url, other.url)

    def __eq__(self, other):
        return self.url == other.urls