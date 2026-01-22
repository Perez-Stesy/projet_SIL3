from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    PromotionViewSet,
    StudentAssignToPromotionView,
    StudentProfileViewSet,
    SubjectViewSet,
)

router = DefaultRouter()
router.register(r"promotions", PromotionViewSet, basename="promotion")
router.register(r"subjects", SubjectViewSet, basename="subject")
router.register(r"students", StudentProfileViewSet, basename="studentprofile")

urlpatterns = [
    path(
        "students/assign/",
        StudentAssignToPromotionView.as_view(),
        name="student-assign-to-promotion",
    ),
    path("", include(router.urls)),
]

