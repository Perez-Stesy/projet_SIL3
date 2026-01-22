from django.contrib import admin

from .models import Promotion, StudentProfile, Subject


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "year", "created_at")
    list_filter = ("year",)
    search_fields = ("name",)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "name")
    search_fields = ("code", "name")


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "promotion", "created_at")
    list_filter = ("promotion__year", "promotion__name")
    search_fields = ("user__email", "user__username", "promotion__name")

from django.contrib import admin

# Register your models here.
