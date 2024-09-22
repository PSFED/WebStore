from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .serializers import *
from .models import *


class GoodsViewSet(viewsets.ModelViewSet):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ("name", "category__name")


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        user = request.user
        cart = Cart.objects.filter(user=user).first()
        if cart:
            serializer = CartSerializer(cart)
            return Response(serializer.data)
        return Response({"detail": "Cart not found"}, status=404)
