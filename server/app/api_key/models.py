import uuid

from django.db import models


class APIKey(models.Model):

    class Meta:
        verbose_name_plural = 'API Keys'
        ordering = ['-created_date']

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_date = models.DateTimeField(auto_now_add=True)

    name = models.CharField(max_length=50, unique=True)
    key = models.CharField(max_length=40, unique=True)
    can_post = models.BooleanField(default=False)
