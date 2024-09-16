import datetime
import uuid
from django.db import models
from django.core.exceptions import ValidationError
from .base_model import BaseModel


class Promocode(BaseModel):
    name = models.CharField(max_length=80)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    expiration_date = models.DateTimeField()
    usage_count = models.IntegerField(default=0)
    code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'

    def __str__(self):
        return f'{self.name} - is_active: {self.is_active} - usages: {self.usage_count}'

    def clean(self):
        super().clean()
        if not isinstance(self.name, str):
            raise TypeError("Name must be a string.")

        if not isinstance(self.expiration_date, datetime.date):
            raise TypeError("Expiration date must be a date.")

        if not isinstance(self.is_active, bool):
            raise TypeError("Is_active must be a boolean.")

        if not isinstance(self.usage_count, int):
            raise TypeError("Usage count must be an integer.")

        if self.discount < 0 or self.discount > 100:
            raise ValidationError('Discount must be in range (1,100) %')
