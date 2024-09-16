import datetime
import pytz

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_at_withTZ = models.DateTimeField(auto_now=True)
    modified_at_withTZ = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save()
        if not self.id:
            self.created_at = timezone.now()
            self.created_at_withTZ = datetime.datetime.now(timezone.timezone.utc).astimezone()
        self.modified_at = timezone.now()
        self.modified_at_withTZ = datetime.datetime.now(timezone.timezone.utc).astimezone()
