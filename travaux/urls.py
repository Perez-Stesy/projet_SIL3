from django.urls import path
from .import views

urlpatterns = [
    
    path('creer/',views.creer_travail, name='creer_travail'),
    path('success/',views.travail_success, name='travail_success'),
]