from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EtudiantViewSet, TravailViewSet

router = DefaultRouter()
router.register(r'etudiants', EtudiantViewSet, basename='etudiant')
router.register(r'travaux', TravailViewSet, basename='travail')

urlpatterns = [
    path('', include(router.urls)),
]
