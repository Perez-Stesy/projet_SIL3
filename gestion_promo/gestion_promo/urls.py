"""
URL configuration for gestion_promo project.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("promotions/", include("promotions.urls")),
]
