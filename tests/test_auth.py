from unittest import TestCase, mock
from datetime import datetime, timedelta
import jwt
from auth.authorizer import handler, generate_aws_policy


class TestAuth(TestCase):
    def build_event(self, token):
        return {
            'authorizationToken': 'bearer ' + token.decode('utf-8')
        }

    def test_validate_invalid_token(self):
        with mock.patch.dict('os.environ', {'SECRET_KEY': '123456789'}):
            payload = {
                'exp': datetime.utcnow() + timedelta(days=1),
                'iat': datetime.utcnow(),
                'sub': '1'
            }

            token = jwt.encode(
                payload,
                '987654321',
                algorithm='HS256'
            )

            event = self.build_event(token)

            self.assertRaises(Exception, handler, event, None)

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

            event = self.build_event(token)

            response = handler(event, None)

            self.assertIsNotNone(response)

    def test_handler_no_token(self):
        event = {
            'event': 'test'
        }

        context = {
            'context': 'text'
        }

        self.assertRaises(Exception, handler, event, context)

    def test_handler_event_is_none(self):
        context = {
            'context': 'text'
        }

        self.assertRaises(Exception, handler, None, context)

    def test_handler_token_is_none(self):
        event = {
            'authorizationToken': None
        }

        context = {
            'context': 'text'
        }

        self.assertRaises(Exception, handler, event, context)
