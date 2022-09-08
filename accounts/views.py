from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework import generics
from rest_framework.views import APIView, Response, status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser
from .permissions import IsOwnerOfTheAccount

from .models import Account
from .serializers import AccountSerializer, LoginSerializer

# Create your views here.


class ListCreateAccountView(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class ListAccountView(generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_queryset(self):
        max_accounts = self.kwargs["num"]
        return self.queryset.order_by("-date_joined")[0:max_accounts]


class UpdateAccountView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerOfTheAccount]

    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    lookup_field = "pk"

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        user = self.get_object()
        self.check_object_permissions(request, user)
        request.data["is_active"] = user.is_active
        return self.update(request, *args, **kwargs)


class UpdateAccountViewAdmin(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    lookup_field = "pk"

    def partial_update(self, request, *args, **kwargs):
        management_user = request.data.pop("is_active")
        request.data.clear()
        request.data["is_active"] = management_user
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )

        if user:
            token, _ = Token.objects.get_or_create(user=user)

            return Response({"token": token.key})

        return Response(
            {"detail": "invalid email or password"}, status.HTTP_401_UNAUTHORIZED
        )
