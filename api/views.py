from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework import viewsets, status
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

    def list(self, request, *args, **kwargs):
        cart, _ = Cart.objects.get_or_create(user=request.user).first()
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    # def add_good(self, request):
    #     user = request.user
    #     good_id = request.data.get("good_id")
    #     quantity = request.data.get("quantity", 1)

    #     try:
    #         item = Goods.objects.get(id=good_id)
    #     except Goods.DoesNotExist:
    #         return Response(
    #             {"detail": "Good not found"}, status=status.HTTP_400_NOT_FOUND
    #         )

    #     cart, created = Cart.objects.get_or_create(user=user)
    #     cart_good, created = CartItem.objects.get_or_create(cart=cart, item=item)
    #     cart_good.quantity += quantity
    #     cart_good.save()

    #     return Response({"detail": "Good not found"}, status=status.HTTP_200_OK)

    # serializer = CartSerializer(data=request.data)
    # serializer.is_valid(raise_exception=True)
    # serializer.save()
    # return Response({"post": serializer.data})
