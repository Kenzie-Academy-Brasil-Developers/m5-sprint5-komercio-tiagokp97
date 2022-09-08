from django.test import TestCase

from accounts.models import Account
from products.models import Product

from rest_framework.views import status


class AccountTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.seller = Account.objects.create_user(
            email="teste@mail.com",
            password="1234",
            first_name="Teste",
            last_name="Final",
            is_seller=True,
        )
        cls.description = "Teste"
        cls.price = "100.99"
        cls.quantity = "15"
        cls.is_active = True

        cls.product = Product.objects.create(
            description=cls.description,
            price=cls.price,
            quantity=cls.quantity,
            is_active=cls.is_active,
            seller=cls.seller,
        )

    def test_account_has_information_fields(self):
        self.product.seller = self.seller
        self.assertEqual(self.product.description, self.description)
        self.assertEqual(self.product.price, self.price)
        self.assertEqual(self.product.quantity, self.quantity)
        self.assertEqual(self.product.is_active, self.is_active)
        self.assertEqual(self.product.seller, self.seller)
