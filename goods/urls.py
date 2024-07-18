from goods.views import category, good
from django.urls import path

app_name = "goods"

urlpatterns = [
    path("", category, name="category"),
    path("good/<slug:good_slug>", good, name="good"),
]
