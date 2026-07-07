from django.db import models


class SessionModel(models.Model):
    session_id = models.UUIDField(unique=True)
    session_data = models.JSONField(default=dict)
    expiration_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
