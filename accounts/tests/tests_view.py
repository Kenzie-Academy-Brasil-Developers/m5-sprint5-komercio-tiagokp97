import json
from rest_framework.test import APITestCase
from accounts.models import Account
from rest_framework.views import status
from rest_framework.authtoken.models import Token


class TestAccountView(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = {
            "email": "marcelo@mail.com",
            "password": "1234",
            "first_name": "marcelo",
            "last_name": "alves",
        }

        cls.public_user = {
            "email": "marcelo2@mail.com",
            "password": "1234",
            "first_name": "marcelo2",
            "last_name": "alves",
        }

    def test_register_account_seller(self):
        self.user["is_seller"] = True
        res = self.client.post("/api/accounts/", data=self.user)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["is_seller"], True)

    def test_register_account_not_seller(self):
        res = self.client.post("/api/accounts/", data=self.user)
        self.assertEqual(res.data["is_seller"], False)

    def test_register_account_missing_keys(self):
        res = self.client.post("/api/accounts/", data={})

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", res.data)
        self.assertIn("password", res.data)
        self.assertIn("first_name", res.data)
        self.assertIn("last_name", res.data)

    def test_login_account_success(self):
        self.user.pop("first_name")
        self.user.pop("last_name")

        new_user = Account.objects.create_user(**self.user)

        res = self.client.post("/api/login/", data=self.user)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(new_user.auth_token.key, res.data["token"])

    def test_only_owner_account_can_update(self):
        owner_user = Account.objects.create_user(**self.user)
        token = Token.objects.create(user=owner_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        data_update = {"first_name": "marcelo123"}
        res = self.client.patch(
            f"/api/accounts/{owner_user.id}/",
            data=json.dumps(data_update),
            content_type="application/json",
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_only_admin_can_disable(self):
        new_user = Account.objects.create_superuser(**self.user)
        token = Token.objects.create(user=new_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        public_user = Account.objects.create_user(**self.public_user)

        data_update = {"is_active": False}
        res = self.client.patch(
            f"/api/accounts/{public_user.id}/management/",
            data=json.dumps(data_update),
            content_type="application/json",
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_only_admin_can_enable(self):
        new_user = Account.objects.create_superuser(**self.user)
        token = Token.objects.create(user=new_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        public_user = Account.objects.create_user(**self.public_user)

        data_update = {"is_active": True}
        res = self.client.patch(
            f"/api/accounts/{public_user.id}/management/",
            data=json.dumps(data_update),
            content_type="application/json",
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_every_one_can_list(self):
        Account.objects.create_user(**self.public_user)
        res = self.client.get("/api/accounts/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
