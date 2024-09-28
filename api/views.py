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
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def get_cart(self, user):
        cart, created = Cart.objects.get_or_create(user=user)
        return cart

    @action(methods=["post"], detail=False, url_path="add-item")
    def add_item(self, request):
        user = request.user
        item_id = request.data.get("item_id")
        quantity = request.data.get("quantity", 1)

        if not item_id:
            return Response(
                {"detail": "item_id is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            item = Goods.objects.get(id=item_id)
        except Goods.DoesNotExist:
            return Response(
                {"detail": "Item not found."}, status=status.HTTP_404_NOT_FOUND
            )

        cart = self.get_cart(user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, good=item)
        if not created:
            cart_item.quantity += int(quantity)
            cart_item.save()
            cart.save()
        else:
            cart_item.quantity = int(quantity)
            cart_item.save()
            cart.save()

        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=["patch"], detail=False)
    def update_item(self, request):
        user = request.user
        item_id = request.data.get("item_id")
        quantity = request.data.get("quantity", 1)

        if not item_id:
            return Response(
                {"detail": "item_id is required."}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            item = Goods.objects.get(id=item_id)
        except Goods.DoesNotExist:
            return Response(
                {"detail": "Item not found."}, status=status.HTTP_404_NOT_FOUND
            )
        cart = self.get_cart(user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, good=item)
        if not created:
            if (
                0 < cart_item.quantity + int(quantity) < cart_item.good.in_stock
                and cart_item.good.availability
            ):
                cart_item.quantity += int(quantity)
                cart_item.save()
            elif 0 >= cart_item.quantity + int(quantity):
                cart_item.delete()
            else:
                return Response(
                    {"detail": "Item is not available."},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            cart_item.quantity = int(quantity)
            cart_item.save()

        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=["delete"], detail=False, url_path="delete")
    def delete_item(self, request):
        user = request.user
        item_id = request.data.get("item_id")

        if not item_id:
            return Response(
                {"detail": "item_id is required."}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            item = Goods.objects.get(id=item_id)
        except Goods.DoesNotExist:
            return Response(
                {"detail": "Item not found."}, status=status.HTTP_404_NOT_FOUND
            )
        cart = self.get_cart(user)
        cart_item = CartItem.objects.filter(cart=cart, good=item)
        cart_item.delete()
        return Response({"detail": str(item) + "deleted"})
