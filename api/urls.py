from django.urls import include, path
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"goods", GoodsViewSet, basename="goods")

urlpatterns = [
    path("", include(router.urls)),
]
