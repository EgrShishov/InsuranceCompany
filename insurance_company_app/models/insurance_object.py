from django.db import models
from .base_model import BaseModel
from . import InsuranceClient


class InsuranceObject(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.ForeignKey(InsuranceClient, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Объект страхования'
        verbose_name_plural = 'Объекты страхования'

    def __str__(self):
        return self.name
