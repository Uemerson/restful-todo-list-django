import uuid

from django.db import models


class TodoList(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=250, blank=False, null=False)
    description = models.CharField(max_length=250, blank=False, null=False)
    concluded = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
