from django.db import models
from django.contrib.auth.models import User


class Categories(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=150, unique=True)

    def __str__(self) -> str:
        return self.name


class Goods(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    discount = models.DecimalField(default=0.00, max_digits=8, decimal_places=2)
    availability = models.BooleanField(default=False)
    in_stock = models.SmallIntegerField(default=0)
    category = models.ForeignKey(to=Categories, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="goods_images")

    def __str__(self) -> str:
        return f"{self.name} | {self.price} | {self.in_stock}"


class Cart(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)


class CartItem(models.Model):
    good = models.ForeignKey(Goods, on_delete=models.CASCADE, related_name="cart_item")
    quantity = models.IntegerField(default=0)
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, blank=True, null=True, related_name="items"
    )

    def __str__(self):
        return str(self.good.name)
