from django.db import models
from .base_model import BaseModel
from django.core.validators import MaxValueValidator, MinValueValidator, MaxLengthValidator, MinLengthValidator


class InsuranceType(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    percentage = models.FloatField()

    class Meta:
        verbose_name = 'Вид страхования'
        verbose_name_plural = 'Виды страхований'

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()
        if self.percentage < 0 or self.percentage > 1:
            raise ValueError('Percentage must be between 0 and 1.')
