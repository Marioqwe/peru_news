from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions

from .models import APIKey


class HasAPIAccess(permissions.BasePermission):
    message = 'Invalid or missing API Key.'

    def has_permission(self, request, view):
        api_key = request.META.get('HTTP_API_KEY', '')
        try:
            api_key = APIKey.objects.get(key=api_key)
            if request.method == 'GET':
                return True
            elif request.method == 'POST':
                return api_key.can_post
            else:
                return False
        except ObjectDoesNotExist:
            # note: set to false to make api private.
            return True
