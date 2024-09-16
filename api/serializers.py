from rest_framework import serializers

from api.models import Goods, Categories, Cart, CartItem


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ("name",)


class GoodsSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer(many=False)

    class Meta:
        model = Goods
        exclude = (
            "image",
            "slug",
        )


class CartItemSerializer(serializers.ModelSerializer):
    total_item_price = serializers.SerializerMethodField(method_name="item_sum")

    class Meta:
        model = CartItem
        fields = "__all__"

    def item_sum(self):
        return self.quantity * (self.good.price * self.good.discount)


class CartSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    created = serializers.DateTimeField(read_only=True)
    items = CartItemSerializer(many=True)
    total_price = serializers.SerializerMethodField(method_name="")

    class Meta:
        model = Cart
        fields = ("created", "total_price")

    def total_price(self, Cart):
        items = Cart.items.all()
        summary = sum(
            [item.quantity * (item.good__price * item.good__discount) for item in items]
        )
        return summary
