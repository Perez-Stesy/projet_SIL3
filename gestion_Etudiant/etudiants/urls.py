from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ajouter/', views.ajouter_etudiant, name='ajouter_etudiant'),
    path('promotion/<int:promotion_id>/classement/', views.classement_promotion, name='classement_promotion'),
    path('api/promotions/', views.api_promotions, name='api_promotions'),
    path('api/promotion/<int:promotion_id>/classement/', views.api_classement, name='api_classement'),
]

