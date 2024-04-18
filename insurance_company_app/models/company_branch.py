from django.db import models
from django.urls import reverse
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
