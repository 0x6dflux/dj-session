from datetime import timedelta

from django.db import models
from django.utils import timezone


def get_expiration_datetime():
    return timezone.now() + timedelta(days=1)


class SessionModel(models.Model):
    session_id = models.UUIDField(unique=True)
    session_data = models.JSONField(default=dict)
    expiration_date = models.DateTimeField(default=get_expiration_datetime)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
