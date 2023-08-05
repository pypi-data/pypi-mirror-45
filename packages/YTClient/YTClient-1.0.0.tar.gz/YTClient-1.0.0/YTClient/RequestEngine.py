from enum import Enum, auto


class RequestType(Enum):
    POST = auto()
    GET = auto()


class RequestEngine(object):
    @staticmethod
    def send_request(http_client, request_type, url, headers, body):
        request_handlers = {RequestType.POST: RequestEngine.post_request,
                            RequestType.GET: RequestEngine.get_request}

        return request_handlers[request_type](http_client, url, headers, body)

    @staticmethod
    def post_request(http_client, url, headers, body):
        resp, content = http_client.request(url,
                                            'POST',
                                            body,
                                            headers)
        return resp, content

    @staticmethod
    def get_request(http_client, url, headers, body=None):
        resp, content = http_client.request(url,
                                            'GET',
                                            body,
                                            headers)
        return resp, content
