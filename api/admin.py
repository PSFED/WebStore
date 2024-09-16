from django.contrib import admin
from .models import Categories, Goods, CartItem


admin.site.register(Categories)
admin.site.register(CartItem)
admin.site.register(Goods)
