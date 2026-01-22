from django.urls import path

from .views import AccountActivationView, MeView, UserCreateView, UserListView

urlpatterns = [
    path("users/", UserCreateView.as_view(), name="accounts-user-create"),
    path("users/list/", UserListView.as_view(), name="accounts-user-list"),
    path("me/", MeView.as_view(), name="accounts-me"),
    path("activate/", AccountActivationView.as_view(), name="accounts-activate"),
]

