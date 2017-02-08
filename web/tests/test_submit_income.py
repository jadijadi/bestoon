from django.test import TestCase, Client

# Models
from web.models import Token, Income
from django.contrib.auth.models import User


class TestIncome(TestCase):
    """
    Class to test submit income api
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

    def test_submit_income_with_correct_request(self):
        context = {
            'text': 'just for testing',
            'amount': '1000',
            'token': 'test_token'
        }

        response = self.client.post(
            '/submit/income', context)

        self.assertEqual(response.status_code, 200)

        all_incomes = Income.objects.all()
        self.assertEqual(all_incomes.count(), 1)

        first_income = all_incomes.first()
        self.assertEqual(first_income.text, context['text'])
        self.assertEqual(first_income.amount, int(context['amount']))

    def test_submit_income_with_incorrect_request_no_text(self):
        context = {
            'amount': '1000',
            'token': 'test_token'
        }

        response = self.client.post(
            '/submit/income', context)

        self.assertEqual(response.status_code, 200)

        all_incomes = Income.objects.all()
        self.assertEqual(all_incomes.count(), 1)

        first_income = all_incomes.first()
        self.assertEqual(first_income.text, "")
        self.assertEqual(first_income.amount, int(context['amount']))

    def test_submit_income_with_incorrect_request_no_amount(self):
        context = {
            'text': 'just for testing',
            'token': 'test_token'
        }

        response = self.client.post(
            '/submit/income', context)

        self.assertEqual(response.status_code, 200)

        all_incomes = Income.objects.all()
        self.assertEqual(all_incomes.count(), 1)

        first_income = all_incomes.first()
        self.assertEqual(first_income.text, context['text'])
        self.assertEqual(first_income.amount, 0)

    def test_submit_income_with_incorrect_request_no_token(self):
        context = {
            'text': 'just for testing',
            'amount': '1000',
        }

        response = self.client.post(
            '/submit/income', context)

        self.assertEqual(response.status_code, 404)

        all_incomes = Income.objects.all()
        self.assertEqual(all_incomes.count(), 0)

    def test_submit_income_with_incorrect_token(self):
        context = {
            'text': 'just for test',
            'amount': '1000',
            'token': 'wrong_token'
        }

        response = self.client.post(
            '/submit/income', context)

        self.assertEqual(response.status_code, 404)

        all_incomes = Income.objects.all()
        self.assertEqual(all_incomes.count(), 0)
