from django.db import models
from .base_model import BaseModel


class FAQ(BaseModel):
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
    added_at = models.DateTimeField()

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return f'{self.question} - {self.answer}'
