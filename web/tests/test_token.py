from django.test import TestCase, Client
import json

# Models
from web.models import Token
from django.contrib.auth.models import User


class TestToken(TestCase):
    """
    Class to test Token model and its usage
    """

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='test',
            email='test@bestoon.ir',
            password='top_secret'
        )
        self.token = Token.objects.create(
            user=self.user,
            token='test_token'
        )

    def test_wrong_token(self):
        response = self.client.post(
            '/accounts/whoami', {
                'token': 'wrong_token'
            })

        self.assertEqual(response.status_code, 404)

    def test_token(self):
        response = self.client.post(
            '/accounts/whoami', {
                'token': self.token.token,
            })

        self.assertEqual(response.status_code, 200)
        response_user = json.loads(response.content)['user']
        self.assertEqual(response_user, self.user.username)
