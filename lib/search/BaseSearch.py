# -*- coding: utf-8 -*-
import thirdparty.requests as requests
import urllib.parse
import threading


class BaseSearch(object):
    # {0} is the query, {1} is the page
    name = "Generic Search Engine"
    uri = 'http://www.example.com/?q={0}&page={1}'
    headers = {'User-agent': 'CHANGEME'}
    data = None
    requester = None
    def __init__(self, query):
        self.query = query
        self.mutex = threading.Lock()
        self.currentPage = 1

    def next(self):
        self.mutex.acquire()
        uri, data = self._formatVars(self.query, self.currentPage)
        body = self._request(uri, data=data)
        captcha = self._isCaptcha(body)
        while captcha:
            self._handleCaptcha(body, uri, data)
            captcha = self._isCaptcha(body)
        self.currentPage += 1
        self.mutex.release()
        results = self._parse(body)
        return results if len(results) > 0 else None

    def _formatVars(self, query, page):
        data = None
        formattedPage = self._formatPage(page)
        formattedQuery = self._formatQuery(query)
        if self.data is not None:
            data = self.data.copy()
            for key, value in data:
                data[key] = value.format(formattedQuery, formattedPage)
        uri = self.uri.format(formattedQuery, formattedPage)
        return uri, data

    def _request(self, uri, headers=None, data=None):
        if self.requester is None:
            self.requester = requests.Session()
            self.requester.headers.update(self.headers)
        response = None
        if data is None:
            response = self.requester.get(uri, headers=headers)
        else:
            response = self.requester.get(uri, headers=headers, data=data)
        return response.content

    def _isCaptcha(self, body):
        return False

    def _formatQuery(self, query):
        return urllib.parse.quote(query)

    def _handleCaptcha(self, body, uri, data=None):
        print ("Fill captcha: {0}".format(uri))
        if data is not None:
            print("Post data: {0}".format(data))
        raw_input ("Press a button when ready")

    def _parse(self, body):
        raise NotImplementedError

    def _formatPage(self, page):
        raise NotImplementedError


