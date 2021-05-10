from django.contrib import admin
from gyoithon.models import Organization


class TargetAdmin(admin.ModelAdmin):
    list_display = ('organization', 'domains', 'overview', 'actions',)
    list_display_links = ('id', 'organization')


admin.site.register(Organization)
