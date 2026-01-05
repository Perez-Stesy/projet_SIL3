from django.urls import path
from .views import creer_formateur

urlpatterns = [
    
    path('creer-formateur/', creer_formateur, name='creer_formateur'),
]