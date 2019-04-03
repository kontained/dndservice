from unittest import TestCase, mock
from datetime import datetime, timedelta
import jwt
from auth.handler import validate, authorize, generate_aws_policy


class TestAuth(TestCase):
    def test_validate_invalid_token(self):
        with mock.patch.dict('os.environ', {'SECRET_KEY': 'f87be322b24b29ee85593f2b976c1737'}):
            payload = {
                'exp': datetime.utcnow() + timedelta(days=1),
                'iat': datetime.utcnow(),
                'sub': '1'
            }

            token = jwt.encode(
                payload,
                'f87be322b24b29ee85593f2b976c1737',
                algorithm='HS256'
            )

            self.assertRaises(
                jwt.exceptions.InvalidSignatureError, validate, token)

    def test_validate_valid_token(self):
        with mock.patch.dict('os.environ', {'SECRET_KEY': '123456789'}):
            payload = {
                'exp': datetime.utcnow() + timedelta(days=1),
                'iat': datetime.utcnow(),
                'sub': '1'
            }

            token = jwt.encode(
                payload,
                '123456789',
                algorithm='HS256'
            )

            result = validate(token)

            self.assertIsNotNone(result)
            self.assertEqual(payload.get('sub'), result.get('sub'))
