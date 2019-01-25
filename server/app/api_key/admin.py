from django.contrib import admin

from .models import APIKey
from .helpers import generate_key


class ApiKeyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'key', 'can_post', 'created_date',)

    fieldsets = (
        ('Required Information', {'fields': ('name', 'can_post')}),
    )

    search_fields = ('id', 'name',)

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def save_model(self, request, obj, form, change):
        if not obj.key:
            obj.key = generate_key()
        obj.save()


admin.site.register(APIKey, ApiKeyAdmin)
