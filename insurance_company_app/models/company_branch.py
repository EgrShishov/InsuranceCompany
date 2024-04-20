import re
from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from .base_model import BaseModel


class CompanyBranch(BaseModel):
    name = models.CharField(max_length=100)
    address = models.TextField()
    phone_number = models.CharField(max_length=16)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Филиал'
        verbose_name_plural = 'Филиалы'

    def get_absolute_url(self):
        return reverse('branch-detail', args=[str(self.id)])

    def clean(self):
        super().clean()

        if not isinstance(self.name, str):
            raise ValidationError('Name value must be string')

        if not isinstance(self.address, str):
            raise ValidationError('Address must be string')

        if not re.match(r'^\+\d{3} \(\d{2}\) \d{3}-\d{2}-\d{2}$', self.phone_number):
            raise ValidationError('Phone number must be in the format +375 (29) XXX-XX-XX')
