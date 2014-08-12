# Class for Google Web Search Parsing
from bs4 import BeautifulSoup
from lib.core import *
import urllib.request
import urllib.parse
import re
import urllib


class GoogleSearch(BaseSearch):
    headers =  {
        'User-Agent': 'Lynx/2.8.8dev.3 libwww-FM/2.14 SSL-MM/1.4.1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-us',
        'Accept-Encoding': 'identity',
        'Keep-Alive': '300',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
    }
    uri = "http://www.google.com/search?q={0}&start={1}&num=100&complete=0"
    

    def _parse(self, body):
        soup = BeautifulSoup(body, "html.parser")
        links = [a for a in soup.findAll('a')]
        results = []
        regmatch = re.compile("^/url\?q=")
        for link in links:
            if None != regmatch.match(link["href"]):
                results.append(SearchResult(url=urllib.parse.unquote(link["href"][7:link["href"].find('&')])))
        return results


    def _formatPage(self, page):
        return (page - 1) * 100