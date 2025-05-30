"""
Django admin page for embargo models
"""

import textwrap

from config_models.admin import ConfigurationModelAdmin
from django.contrib import admin

from .forms import IPFilterForm, RestrictedCourseForm
from .models import CountryAccessRule, GlobalRestrictedCountry, IPFilter, RestrictedCourse


class IPFilterAdmin(ConfigurationModelAdmin):
    """Admin for blacklisting/whitelisting specific IP addresses"""
    form = IPFilterForm
    fieldsets = (
        (None, {
            'fields': ('enabled', 'whitelist', 'blacklist'),
            'description': textwrap.dedent("""Enter specific IP addresses to explicitly
            whitelist (not block) or blacklist (block) in the appropriate box below.
            Separate IP addresses with a comma. Do not surround with quotes.
            """)
        }),
    )


class CountryAccessRuleInline(admin.StackedInline):
    """Inline editor for country access rules. """
    model = CountryAccessRule
    extra = 1

    def has_delete_permission(self, request, obj=None):
        return True


class RestrictedCourseAdmin(admin.ModelAdmin):
    """Admin for configuring course restrictions. """
    inlines = [CountryAccessRuleInline]
    form = RestrictedCourseForm
    search_fields = ('course_key',)


class GlobalRestrictedCountryAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Global Country Restriction model.
    """
    list_display = ("country",)

    def delete_queryset(self, request, queryset):
        """
        Override the delete_queryset method to clear the cache when objects are deleted in bulk.
        """
        super().delete_queryset(request, queryset)
        GlobalRestrictedCountry.update_cache()


admin.site.register(IPFilter, IPFilterAdmin)
admin.site.register(RestrictedCourse, RestrictedCourseAdmin)
admin.site.register(GlobalRestrictedCountry, GlobalRestrictedCountryAdmin)
