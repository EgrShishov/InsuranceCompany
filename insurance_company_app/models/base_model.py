import datetime
from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now()) #.strftime('%DD/%MM/%YYYY')
    updated_at = models.DateTimeField(auto_now=True)
    created_at_withTZ = models.DateTimeField(default=datetime.datetime.now(timezone.timezone.utc).astimezone())
    updated_at_withTZ = models.DateTimeField(auto_now=True)
