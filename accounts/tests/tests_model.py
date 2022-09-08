from django.test import TestCase

from accounts.models import Account
from rest_framework.views import status


class AccountTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.email = "teste@mail.com"
        cls.password = "1234"
        cls.first_name = "Teste"
        cls.last_name = "Final"
        cls.is_seller = 'True'

        cls.account = Account.objects.create(
            email=cls.email,
            password = cls.password,
            first_name=cls.first_name,
            last_name=cls.last_name,
            is_seller=cls.is_seller,
        )

    def test_account_has_information_fields(self):              
        self.assertEqual(self.account.email, self.email)
        self.assertEqual(self.account.password, self.password)
        self.assertEqual(self.account.first_name, self.first_name)
        self.assertEqual(self.account.last_name, self.last_name)
        self.assertEqual(self.account.is_seller, self.is_seller)