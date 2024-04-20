from django.core.exceptions import ValidationError
from django.db import models
from .base_model import BaseModel
from .insurance_client import InsuranceClient


class Review(BaseModel):
    text = models.TextField()
    author = models.ForeignKey(InsuranceClient, on_delete=models.CASCADE)
    rating = models.IntegerField()

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'Review by {self.author.surname} - Rating: {self.rating}'

    def clean(self):
        super().clean()

        if not 11 > self.rating > 0:
            raise ValidationError('Rate must be in interval (0,10)')

