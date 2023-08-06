from .client import Client


class Resource(object):
    def __init__(
        self,
        client,
        api_version='v0',
        path=None,
        auth_required=True,
        name=None
    ):
        self.client = client
        self.api_version = api_version
        self.path = path
        if not path:
            self.path = ''
        self.auth_required = auth_required
        self.name = name

    def _assemble_uri(
        self,
        resource_id=None
    ):
        path = [self.client.api_root]

        if self.api_version:
            path.append(self.api_version)

        path_formatted = self.path.strip('/')
        path.append(self.path)

        if resource_id:
            path.append(resource_id)

        path.append('')

        return '/'.join(path)

    def request(
        self,
        method,
        data={},
        headers={},
        resource_id=None
    ):
        if (
            not self.auth_required and
            not self.client.get_credentials() and
            self.client.api_key
        ):
            data['client_id'] = self.client.api_key

        uri = self._assemble_uri(resource_id=resource_id)

        return self.client.request(
            method,
            uri,
            data,
            headers
        )

    def create(
        self,
        data={},
        headers={}
    ):
        method = 'post'
        return self.request(
            method,
            data=data,
            headers=headers
        )

    def update(
        self,
        resource_id,
        data={},
        headers={}
    ):
        method = 'put'
        return self.request(
            method,
            data=data,
            headers=headers,
            resource_id=resource_id
        )

    def retrieve(
        self,
        resource_id=None,
        data={},
        headers={}
    ):
        method = 'get'
        return self.request(
            method,
            data=data,
            headers=headers,
            resource_id=resource_id
        )

    def destroy(
        self,
        resource_id,
        data={},
        headers={}
    ):
        method = 'delete'
        return self.request(
            method,
            data=data,
            headers=headers,
            resource_id=resource_id
        )

    def options(
        self,
        data,
        headers
    ):
        method = 'options'
        return self.request(
            method,
            data=data,
            headers=headers
        )
