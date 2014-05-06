class Response:
    def __init__(self, status, reason, headers, body):
        self.status = status
        self.reason = reason
        self.headers = headers
        self.body = body


    def __str__(self):
        return self.body


    def __int__(self):
        return self.status


    def __eq__(self, other):
        return (self.headers == other.headers) and (self.body == other.body) and (self.status == other.status11)