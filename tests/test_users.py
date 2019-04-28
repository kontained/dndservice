from unittest import TestCase, mock
from common.users.usermodel import User
from bcrypt import hashpw, checkpw, gensalt


class TestUsers(TestCase):
    def test_pynamodb_table_create(self):
        with mock.patch.dict('os.environ', {'DYNAMODB_URL': 'http://localhost:8000'}):
            if not User.exists():
                User.create_table(wait=True)

    def test_pynamodb_user_create(self):
        user = User(username='TEST', password_hash='TEST', refresh_token='token')
        user.save()

    def test_pynamodb_username_query(self):
        for user in User.username_index.query('TEST'):
            self.assertIsNotNone(user)

    def test_pynamodb_user_id_query(self):
        for user in User.query('15e96c96-ec45-4a48-99ee-dde160b72bfd'):
            self.assertIsNotNone(user)

    def test_pynamodb_hashed_password(self):
        hashed = hashpw('password'.encode(), gensalt())

        result = checkpw('password'.encode(), hashed)

        print(result)
