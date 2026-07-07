from datetime import timedelta
from uuid import uuid4

from django.conf import settings
from django.db import models
from django.utils import timezone


def get_expiration_datetime():
    return timezone.now() + timedelta(days=1)


class SessionModel(models.Model):
    session_id = models.UUIDField(unique=True, default=uuid4)
    session_data = models.JSONField(default=dict)
    expiration_date = models.DateTimeField(default=get_expiration_datetime)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.CASCADE,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
