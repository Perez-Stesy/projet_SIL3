from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/promotions/', views.api_list_promotions, name='api_list_promotions'),
    path('api/promotions/create/', views.api_create_promotion, name='api_create_promotion'),
    path('api/promotions/<int:promotion_id>/', views.api_get_promotion, name='api_get_promotion'),
    path('api/promotions/<int:promotion_id>/update/', views.api_update_promotion, name='api_update_promotion'),
    path('api/promotions/<int:promotion_id>/delete/', views.api_delete_promotion, name='api_delete_promotion'),
]
