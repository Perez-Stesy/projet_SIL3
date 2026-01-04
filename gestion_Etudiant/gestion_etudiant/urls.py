"""
URL configuration for gestion_etudiant project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('etudiants.urls')),
]

