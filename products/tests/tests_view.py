from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework.views import APIView, Response, status
import json

from accounts.models import Account
from products.models import Product


class TestAccountView(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = {
            "email": "marcelo@mail.com",
            "password": "1234",
            "first_name": "marcelo",
            "last_name": "alves",
        }

        cls.product = {"description": "Teste", "price": 100.99, "quantity": 15}

    def test_only_seller_can_create(self):
        self.user["is_seller"] = True
        seller_user = Account.objects.create_user(**self.user)
        token = Token.objects.create(user=seller_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        res = self.client.post(
            f"/api/products/",
            data=self.product,
        )

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_only_seller_can_update(self):
        self.user["is_seller"] = True
        seller_user = Account.objects.create_user(**self.user)
        token = Token.objects.create(user=seller_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        product_user = Product.objects.create(**self.product, seller=seller_user)

        data_product = {"description": "Smartband XYZ 1000"}

        res = self.client.patch(
            f"/api/products/{product_user.id}/",
            data=json.dumps(data_product),
            content_type="application/json",
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_list_products(self):
        self.user["is_seller"] = True
        seller_user = Account.objects.create_user(**self.user)
        token = Token.objects.create(user=seller_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        Product.objects.create(**self.product, seller=seller_user)

        res = self.client.get(f"/api/products/")

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_list_specify_product(self):
        self.user["is_seller"] = True
        seller_user = Account.objects.create_user(**self.user)
        token = Token.objects.create(user=seller_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        product_user = Product.objects.create(**self.product, seller=seller_user)

        res = self.client.get(f"/api/products/{product_user.id}/")

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_register_product_missing_keys(self):
        self.user["is_seller"] = True
        seller_user = Account.objects.create_user(**self.user)
        token = Token.objects.create(user=seller_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        res = self.client.post(
            f"/api/products/",
            data={},
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("description", res.data)
        self.assertIn("price", res.data)
        self.assertIn("quantity", res.data)

    def test_register_negative_quantity(self):
        self.user["is_seller"] = True
        seller_user = Account.objects.create_user(**self.user)
        token = Token.objects.create(user=seller_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        self.product["quantity"] = -1

        res = self.client.post(
            f"/api/products/",
            data=self.product,
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


