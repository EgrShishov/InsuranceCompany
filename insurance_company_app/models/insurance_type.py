from django.db import models
from .base_model import BaseModel


class InsuranceType(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    percentage = models.FloatField()

    class Meta:
        verbose_name = 'Вид страхования'
        verbose_name_plural = 'Виды страхований'

    def __str__(self):
        return self.name
