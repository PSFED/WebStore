from rest_framework import serializers
from api.models import Goods, Categories, Cart, CartItem


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ("name",)


class GoodsSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer()

    class Meta:
        model = Goods
        # fields = (
        #     "name",
        #     "description",
        #     "price",
        #     "discount",
        #     "availability",
        #     "in_stock",
        #     "category",
        # )
        exclude = (
            "image",
            "slug",
        )


class CartItemSerializer(serializers.ModelSerializer):
    total_item_price = serializers.SerializerMethodField(method_name="sum")
    good = GoodsSerializer()

    class Meta:
        model = CartItem
        fields = "__all__"

    def sum(self, cart_item):
        return (cart_item.quantity * cart_item.good.price) * (
            1 - cart_item.good.discount / 100
        )


class CartSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    created = serializers.DateTimeField(read_only=True)
    items = CartItemSerializer(many=True)
    total_price = serializers.SerializerMethodField(method_name="total")
    user = serializers.CharField(read_only=True)

    class Meta:
        model = Cart
        fields = "__all__"

    def total(self, cart):
        items = cart.items.all()
        summary = sum(
            [
                (item.quantity * item.good.price) * (1 - item.good.discount / 100)
                for item in items
            ]
        )
        return summary
