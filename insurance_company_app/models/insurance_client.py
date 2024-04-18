from django.db import models
from .base_model import BaseModel


class InsuranceClient(BaseModel):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=40)
    second_name = models.CharField(max_length=40)
    age = models.IntegerField()
    address = models.TextField()
    phone_number = models.CharField(max_length=16)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return self.name