from unittest import TestCase


class TestClientClass(TestCase):
    def test_is_resource_defined(self):
        from librestapi import Resource
        self.assertTrue(Resource)

    def test_define_resource(self):
        from librestapi import Client, Resource

        client = Client(api_root='https://jsonplaceholder.typicode.com')

        Photos = Resource(
            client,
            api_version=None,
            auth_required=False,
            path='photos',
            name='photos'
        )

        response = Photos.retrieve()
