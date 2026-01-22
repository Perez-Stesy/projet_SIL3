from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PedagogicalSpaceViewSet

router = DefaultRouter()
router.register(r"spaces", PedagogicalSpaceViewSet, basename="pedagogical-space")

urlpatterns = [
    path("", include(router.urls)),
]

