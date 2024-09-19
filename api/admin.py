from django.contrib import admin
from .models import Cart, Categories, Goods, CartItem


admin.site.register(Categories)
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(Goods)
