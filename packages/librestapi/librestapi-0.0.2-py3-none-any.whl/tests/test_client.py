from unittest import TestCase


class TestClientClass(TestCase):
    def test_is_client_defined(self):
        from librestapi import Client
        self.assertTrue(Client)

    def test_constructor(self):
        from librestapi import Client

        api_key = 'test_api_key',
        api_secret = 'test_api_secret'
        api_root = 'testroot.com/'
        auth_uri = 'testroot.com/auth'
        
        client = Client(
            api_key=api_key,
            api_secret=api_secret,
            api_root=api_root,
            auth_uri=auth_uri
        )

        self.assertEqual(client.api_key, api_key)
        self.assertEqual(client.api_secret, api_secret)
        self.assertEqual(client.api_root, api_root)
        self.assertEqual(client.auth_uri, auth_uri)
        self.assertIsNone(client.credentials)

    def test_credentials(self):
        from librestapi import Client
        client = Client()

        self.assertIsNone(client.credentials)
        self.assertIsNone(client.get_credentials())

        credentials = {
            'some-key': 'and value',
            'pairs-that': 'represent credentials'
        }

        client.set_credentials(**credentials)

        self.assertEqual(
            credentials,
            client.credentials
        )

        client.invalidate_credentials()

        self.assertIsNone(client.credentials)
        self.assertIsNone(client.get_credentials())

    def test_assemble_headers(self):
        from librestapi import Client

        client = Client()

        headers = client._assemble_headers()

        self.assertEqual({
            'Accept': 'application/json'
        }, headers)

        credentials = {
            'access_token': 'test_access_token',
            'current_identity': 'test_current_identity'
        }

        client.set_credentials(**credentials)

        self.assertEqual({
            'Accept': 'application/json',
            'Current-Identity': credentials['current_identity'],
            'Authorization': 'Bearer ' + credentials['access_token'],
            'TestHeader': 'test_header'
        }, client._assemble_headers(**{'TestHeader': 'test_header'}))

    def test_request(self):
        from librestapi import Client

        client = Client()
        credentials = {
            'access_token': 'test_access_token',
            'current_identity': 'test_current_identity'
        }

        client.set_credentials(**credentials)
        response = client.request(
            'get',
            'https://example.com',
            {}, {
                'test-header': 'test-header=value'
            }
        )
