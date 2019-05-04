from unittest import TestCase, mock
import json
from users.login import handler


class TestLogin(TestCase):
    def test_no_username(self):
        event = {
            'body': json.dumps({
                'password': 'test'
            })
        }

        self.assertRaises(Exception, handler, event, None)

    def test_no_password(self):
        event = {
            'body': json.dumps({
                'username': 'test'
            })
        }

        self.assertRaises(Exception, handler, event, None)

    @mock.patch.dict('os.environ', {'SECRET_KEY': '123456789', 'REFRESH_KEY': '987654321'})
    def test_login(self):
        event = {
            'body': json.dumps({
                'username': 'test',
                'password': 'test'
            })
        }

        result = handler(event, None)
        body = json.loads(result.get('body'))

        self.assertIsNotNone(result)
        self.assertIsNotNone(body.get('access_token'))

    def test_login_bad_credentials(self):
        event = {
            'body': json.dumps({
                'username': 'test',
                'password': 'test'
            })
        }

        self.assertRaises(Exception, handler, event, None)
