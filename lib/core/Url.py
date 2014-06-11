import urllib.parse

class Url(object):
    def __init__(self, url):
        parsed = urllib.parse.urlparse(url)
        self.params = {v[0] : ("" if len(v) < 2 else v[1]) for v in (t.split('=', 1) for t in parsed.query.split('&'))  if v[0] is not "" }
        self.paramNames = '&'.join(key for key in self.params.keys())
        self.scheme = parsed.scheme
        self.netloc = parsed.netloc
        self.path = parsed.path

    def __str__(self):
        params = '&'.join(("" if key is "" else key + '=') + ("" if value is None else value) for key, value in self.params.items())
        return self.scheme + self.netloc + self.path + ('?' + params if params is not "" else "")

    def __eq__(self, other):
        return self.params == other.params and self.scheme == other.scheme and self.netloc == other.netloc and self.path == other.path

    def getWithoutParamValues(self):
        params = '&'.join(("" if key is "" else key + '=') for key, value in self.params.items())
        return self.scheme + self.netloc + self.path + ('?' + params if params is not "" else "")

    def compareParamNames(self, other):
        return self.paramNames == other.paramNames and self.scheme == other.scheme and self.netloc == other.netloc and self.path == other.path

    def hasParameters(self):
        return len(self.params) > 0

    def hasIntegerValue(self):
        return any([value.isdigit() for value in self.params.values()])