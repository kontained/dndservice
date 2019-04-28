from unittest import TestCase, mock
from jwt import ExpiredSignatureError, DecodeError
from datetime import datetime
from common.token.factory import create_user_token, validate_user_token
from common.users.usermodel import User


class TestToken(TestCase):
    def build_user(self):
        return User(
            user_id=1,
            username='test',
            password_hash='test'
        )

    def test_create_user_token_not_user_instance(self):
        with self.assertRaises(AttributeError):
            create_user_token('1')

    def test_create_user_token(self):
        with mock.patch.dict('os.environ', {'SECRET_KEY': '123456789'}):
            result = create_user_token(self.build_user())
            self.assertTrue(isinstance(result, bytes))

    def test_decode_token(self):
        with mock.patch.dict('os.environ', {'SECRET_KEY': '123456789'}):
            token = create_user_token(self.build_user())
            result = validate_user_token(token)
            self.assertIsNotNone(result)

    @mock.patch('common.token.factory.datetime')
    def test_decode_expired_token(self, mock_datetime):
        with mock.patch.dict('os.environ', {'SECRET_KEY': '123456789'}):
            mock_datetime.utcnow = mock.Mock(return_value=datetime(2010, 1, 1))
            token = create_user_token(self.build_user())
            self.assertRaises(ExpiredSignatureError, validate_user_token, token)

    def test_decode_modified_token(self):
        with mock.patch.dict('os.environ', {'SECRET_KEY': '123456789'}):
            token = create_user_token(self.build_user())
            test = bytearray(token)
            test[0] = 100
            self.assertRaises(DecodeError, validate_user_token, bytes(test))
