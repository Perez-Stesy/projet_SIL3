from django.contrib import admin

from .models import PedagogicalSpace


@admin.register(PedagogicalSpace)
class PedagogicalSpaceAdmin(admin.ModelAdmin):
    list_display = ("id", "subject", "year", "promotion", "created_at")
    list_filter = ("year", "promotion__name", "promotion__year")
    search_fields = ("subject__code", "subject__name", "promotion__name")
from django.contrib import admin

# Register your models here.
