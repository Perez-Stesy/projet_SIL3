from django.urls import path
from .import views

urlpatterns=[
    path('evaluer/<int:travail_id>/', views.evaluer_travail, name='evaluer_travail'),
    path('success/', views.evaluation_success, name='evaluation_success'),
]