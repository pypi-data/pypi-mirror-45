import requests
from io import BytesIO


class Response(object):
    def __init__(
        self,
        response,
        data,
        content_type,
        status
    ):
        self._response = response
        self.data = data,
        self.content_type = content_type
        self.status = status
        

class Credentials(object):
    def __init__(
        self,
        access_token,
        current_identity
    ):
        self.access_token = access_token
        self.current_identity = current_identity


class Client(object):
    def __init__(
        self,
        api_key=None,
        api_secret=None,
        api_root='/',
        auth_uri=None,
        *args,
        **kwargs
    ):
        self.api_key = api_key
        self.api_secret = api_secret
        self.api_root = api_root
        self.auth_uri = auth_uri
        self.credentials = None

    def get_credentials(self):
        return self.credentials

    def set_credentials(
        self,
        **credentials
    ):
        self.credentials = credentials

    def invalidate_credentials(self):
        self.credentials = None

    def _assemble_headers(
        self,
        **headers
    ):
        if not headers:
            headers = {}

        credentials = self.get_credentials()
        if credentials:
            access_token = credentials.get('access_token')
            if access_token:
                headers['Authorization'] = ' '.join([
                    'Bearer',
                    access_token
                ])

            current_identity = credentials.get('current_identity')
            if current_identity:
                headers['Current-Identity'] = current_identity

        headers['Accept'] = 'application/json'

        return headers

    def request(
        self,
        method,
        uri,
        data,
        headers
    ):
        headers = self._assemble_headers(**headers)

        method_func = getattr(requests, method.lower(), None)

        if None is method_func:
            raise Client.MethodNotSupportedException(method)

        request_args = {}

        if None is not data:
            request_args['data'] = data

        response = method_func(uri, **request_args)
        response.raise_for_status()
        
        response_headers = response.headers
        content_type = response_headers.get('content-type')

        if 'text/' in content_type:
            response_data = response.text

        elif (
            'application/octet-stream' == content_type or
            'image/' in content_type or
            'audio/' in content_type or
            'video/' in content_type or
            '/ogg' in content_type
        ):
            response_data = BytesIO(response.content)

        elif 'application/json' == content_type:
            response_data = response.json()

        else:
            response_data = response.content

        return Response(
            response,
            response_data,
            content_type,
            response.status_code
        )

    class MethodNotSupportedException(Exception):
        def __init__(self, method, *args, **kwargs):
            super(MethodNotSupportedException, self).__init__(' '.join([
                'ERROR: Method',
                method,
                'not supported by requests.'
            ]))

            self.method = method
