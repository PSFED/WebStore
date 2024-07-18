from django.db import models


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
