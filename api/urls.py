from django.urls import include, path
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"goods", GoodsViewSet, basename="goods")
router.register(r"carts", CartViewSet, basename="carts")

urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("rest_framework.urls")),
]
