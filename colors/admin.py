from django.contrib import admin
from .models import Color


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = (
        'hex_code',
        'r',
        'g',
        'b',
        'created_at',
        'times_discovered',
    )