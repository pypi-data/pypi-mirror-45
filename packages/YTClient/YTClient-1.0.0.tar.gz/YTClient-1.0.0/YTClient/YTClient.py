import json
import urllib.parse
import httplib2 as httplib2


from http.client import HTTPException

from YTClient.YTDataClasses import Project, Command
from YTClient.RequestEngine import RequestEngine, RequestType


class YTException(HTTPException):
    def error_code(self):
        return self.response.status

    def error(self):
        return self.content['error']

    def error_description(self):
        return self.content['error_description']

    def __init__(self, response, content):
        self.response = response
        self.content = content

    def __repr__(self):
        return "Code: {code}, Error: {error}, Error Description: {description}" \
                .format(code=self.error_code(),
                        error=self.error(),
                        description=self.error_description())

    def __str__(self):
        return self.__repr__()


class YTClient(object):
    FIELDS_PARAMETER = 'fields'

    def __init__(self, url, proxy_info=None, token=None):
        if proxy_info:
            self.http_client = httplib2.Http(disable_ssl_certificate_validation=True, proxy_info=proxy_info)
        else:
            self.http_client = httplib2.Http(disable_ssl_certificate_validation=True)

        self.baseUrl = url.rstrip('/')
        self.apiUrl = self.baseUrl + '/api'
        self.headers = dict()
        self.__last_credentials = None

        self.set_auth_token(token)

        self.headers['Accept'] = 'application/json'
        self.headers['Content-Type'] = 'application/json'

    def set_auth_token(self, token):
        if token:
            self.headers = {'Authorization': 'Bearer {}'.format(token)}

    def create_issue(self, project: Project, summary: str, description: str = None, additional_fields: dict = None,
                     return_fields: list = None):
        issue_info = {'project': project._asdict(),
                      'summary': summary,
                      'description': description}

        if additional_fields:
            issue_info = {**issue_info, **additional_fields}

        self.headers['Cache-Control'] = 'no-cache'

        if return_fields:
            return_fields = {self.FIELDS_PARAMETER: ','.join(return_fields)}

        return self.__request(RequestType.POST, '/issues', return_fields, issue_info)

    def run_command(self, command: Command, return_fields: list = None):
        command_dict = command._asdict()

        if return_fields:
            return_fields = {self.FIELDS_PARAMETER: ','.join(return_fields)}

        return self.__request(RequestType.POST, '/commands', return_fields, command_dict)

    def get_issues(self, query: str, fields: list = None, skip: int = None, top: int = None):
        return_fields = {'query': query}

        if fields:
            return_fields[self.FIELDS_PARAMETER] = ','.join(fields)
        if skip:
            return_fields['$skip'] = skip
        if top:
            return_fields['$top'] = top

        return self.__request(RequestType.GET, '/issues', return_fields)

    def get_projects(self, fields: list = None, skip: int = None, top: int = None):
        return_fields = dict()

        if fields:
            return_fields[self.FIELDS_PARAMETER] = ','.join(fields)
        if skip:
            return_fields['$skip'] = skip
        if top:
            return_fields['$top'] = top

        return self.__request(RequestType.GET, '/admin/projects', return_fields)

    def __request(self, request_type, resource, request_prams=None, request_body=None):
        if resource.startswith('http'):
            request_url = resource
        else:
            request_url = self.apiUrl + resource

        if request_prams:
            request_url += '?' + urllib.parse.urlencode(request_prams)

        body_json = None
        if request_body:
            body_json = json.dumps(request_body)

        resp, json_content = RequestEngine.send_request(self.http_client, request_type, request_url, self.headers,
                                                        body_json)
        content = json.loads(json_content)

        if resp.status != 200:
            raise YTException(resp, content)

        return content
