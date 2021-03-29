from django.contrib import admin
from atd.models import Target


class TargetAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'overview', 'last_scan_date', 'status',)
    list_display_links = ('id', 'name')


admin.site.register(Target, TargetAdmin)
