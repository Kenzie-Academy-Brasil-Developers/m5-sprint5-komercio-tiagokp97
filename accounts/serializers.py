from rest_framework import serializers

from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "is_seller",
            "date_joined",
            "is_active"
        ]
        extra_kwargs = {"password": {"write_only": True}}
        

    def create(self, validated_data: dict) -> Account:
        return Account.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100)
    password = serializers.CharField(write_only=True)
