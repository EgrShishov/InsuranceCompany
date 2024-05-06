from django.db import models
from .base_model import BaseModel


class InsuranceObject(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        verbose_name = 'Объект страхования'
        verbose_name_plural = 'Объекты страхования'

    def __str__(self):
        return self.name

