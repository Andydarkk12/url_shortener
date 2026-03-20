from django.contrib import admin

from django.contrib import admin
from .models import ShortLink

@admin.register(ShortLink)
class ShortLinkAdmin(admin.ModelAdmin):
    list_display = ('short_url', 'original_url', 'clicks', 'created_at')
    search_fields = ('short_url', 'original_url')
    readonly_fields = ('clicks', 'created_at')
