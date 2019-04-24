from unittest import TestCase, mock
from users.register import handler


class TestRegister(TestCase):
    @mock.patch('users.usermodel.User')
    def test_mock(self, mockUser):
        pass