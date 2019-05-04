from unittest import TestCase, mock
import json
import os
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

    @mock.patch('common.users.usermodel.User.username_index.query')
    def test_pynamodb_throws_exception(self, mockUser):
        mockUser.side_effect = Exception('Test')

        event = {
            'body': json.dumps({
                'username': 'test',
                'password': 'test'
            })
        }

        self.assertRaises(Exception, handler, event, None)

    @mock.patch.dict('os.environ', {'SECRET_KEY': '123456789', 'REFRESH_KEY': '987654321'})
    @mock.patch('common.users.usermodel.User.username_index.query')
    @mock.patch('common.users.usermodel.User.save')
    def test_user_creation(self, mockSave, mockQuery):
        mockSave.return_value = True
        mockQuery.return_value = []

        event = {
            'body': json.dumps({
                'username': 'test',
                'password': 'test'
            })
        }

        result = handler(event, None)
        body = json.loads(result.get('body'))

        self.assertIsNotNone(result)
        self.assertEqual(result.get('statusCode'), 200)
        self.assertIsNotNone(body.get('user_id'))
        self.assertIsNotNone(body.get('access_token'))
        self.assertIsNotNone(body.get('refresh_token'))

    @mock.patch.dict('os.environ', {'SECRET_KEY': '123456789', 'REFRESH_KEY': '987654321'})
    @mock.patch('common.users.usermodel.User.username_index.query')
    @mock.patch('common.users.usermodel.User.save')
    def test_save_throws_exception(self, mockSave, mockQuery):
        mockSave.side_effect = Exception('test')
        mockQuery.return_value = []

        event = {
            'body': json.dumps({
                'username': 'test',
                'password': 'test'
            })
        }

        self.assertRaises(Exception, handler, event, None)
