from django.contrib import admin
from goods.models import Categories, Goods


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
