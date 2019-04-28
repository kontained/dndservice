from unittest import TestCase, mock
import json
from users.register import handler


class TestRegister(TestCase):
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

    @mock.patch('common.users.usermodel.User.username_index.query')
    def test_username_already_exists(self, mockUser):
        mockUser.return_value = [
            {
                'test': 'me'
            }
        ]

        event = {
            'body': json.dumps({
                'username': 'test',
                'password': 'test'
            })
        }

        self.assertRaises(Exception, handler, event, None)
