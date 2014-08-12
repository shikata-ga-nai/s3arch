# Class for Bing  Web Search Parsing
from bs4 import BeautifulSoup
from lib.core import *
import urllib.request
import urllib.parse
import re
import urllib

class BingSearch(BaseSearch):
	headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:11.0) Gecko/20100101 Firefox/11.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-us',
        'Accept-Encoding': 'identity',
        'Keep-Alive': '300',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
    }

	uri = 'http://www.bing.com/search?q={0}&first={1}&go=&qs=n&FORM=PORE'

	def _parse(self, body):
		soup = BeautifulSoup(body, "html.parser")
		results = []
		lis = [li for li in soup.findAll('li', attrs={"class" : "b_algo"})]
		for li in lis:
			a = li.find("a")
			results.append(SearchResult(url=a["href"]))
		return results

#        results = []
#        regmatch = re.compile("^/url\?q=")
#        for link in links:
#            if None != regmatch.match(link["href"]):
#                results.append(SearchResult(url=urllib.parse.unquote(link["href"][7:link["href"].find('&')])))
#        return results

	def _formatPage(self, page):
		return ((page - 1) * 50) + 1