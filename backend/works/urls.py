from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    PromotionRankingView,
    StudentMyEvaluationsView,
    StudentMyAssignmentsView,
    StudentMySubmissionsView,
    TrainerMySubmissionsView,
    EvaluationCreateView,
    SubmissionCreateView,
    WorkAssignmentViewSet,
    WorkViewSet,
)

router = DefaultRouter()
router.register(r"works", WorkViewSet, basename="work")
router.register(r"assignments", WorkAssignmentViewSet, basename="assignment")

urlpatterns = [
    path("", include(router.urls)),
    path("me/assignments/", StudentMyAssignmentsView.as_view(), name="me-assignments"),
    path("me/submissions/", StudentMySubmissionsView.as_view(), name="me-submissions"),
    path("me/submissions/formateur/", TrainerMySubmissionsView.as_view(), name="me-submissions-formateur"),
    path("me/evaluations/", StudentMyEvaluationsView.as_view(), name="me-evaluations"),
    path("submissions/", SubmissionCreateView.as_view(), name="submission-create"),
    path("evaluations/", EvaluationCreateView.as_view(), name="evaluation-create"),
    path("ranking/", PromotionRankingView.as_view(), name="promotion-ranking"),
]

