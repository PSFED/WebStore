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
    total_item_price = serializers.SerializerMethodField(method_name="sum")
    good = GoodsSerializer(many=False)

    class Meta:
        model = CartItem
        fields = "__all__"

    # def sum(self):
    #     return self.quantity * (self.good.price * self.good.discount)

    def sum(self, CartItem):
        sum = (CartItem.quantity * CartItem.good.price) * (
            1 - CartItem.good.discount / 100
        )
        return sum


class CartSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    created = serializers.DateTimeField(read_only=True)
    items = CartItemSerializer(many=True)
    total_price = serializers.SerializerMethodField(method_name="total")
    user = serializers.CharField()

    class Meta:
        model = Cart
        fields = "__all__"

    def total(self, Cart):
        items = Cart.items.all()
        summary = sum(
            [
                (item.quantity * item.good.price) * (1 - item.good.discount / 100)
                for item in items
            ]
        )
        return summary
