from django.contrib import admin

from .models import Evaluation, Submission, Work, WorkAssignment


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "type", "space", "created_by", "due_at", "created_at")
    list_filter = ("type", "space__year", "space__subject__code")
    search_fields = ("title", "space__subject__code", "created_by__email")


@admin.register(WorkAssignment)
class WorkAssignmentAdmin(admin.ModelAdmin):
    list_display = ("id", "work", "student", "assigned_at")
    list_filter = ("work__space__year", "work__space__subject__code")
    search_fields = ("student__user__email", "work__title")


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("id", "assignment", "submitted_at")
    search_fields = ("assignment__student__user__email", "assignment__work__title")


@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ("id", "submission", "evaluator", "grade", "max_grade", "published", "evaluated_at")
    list_filter = ("published", "submission__assignment__work__space__year")
    search_fields = ("evaluator__email", "submission__assignment__student__user__email")

from django.contrib import admin

# Register your models here.
