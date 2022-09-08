from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from accounts.permissions import IsSelleOfTheProduct, IsSeller

from products.mixins import SerializerByMethodMixin

from .models import Product
from .serializers import ProductCreateSerializer, ProductListSerializer


class ListCreateProductView(SerializerByMethodMixin, generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsSeller]

    queryset = Product.objects.all()

    serializer_map = {
        "GET": ProductListSerializer,
        "POST": ProductCreateSerializer,
    }

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

    
class RetrieveUpdateProductView(
    SerializerByMethodMixin, generics.RetrieveUpdateAPIView
):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsSelleOfTheProduct]
    queryset = Product.objects.all()
    serializer_map = {
        "GET": ProductListSerializer,
        "PATCH": ProductCreateSerializer,
    }
