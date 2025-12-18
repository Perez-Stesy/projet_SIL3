from django.urls import path
from .views import promotion_create, promotion_success

app_name = "promotions"

urlpatterns = [
    path("create/", promotion_create, name="promotion_create"),
    path("success/", promotion_success, name="promotion_success"),
]

