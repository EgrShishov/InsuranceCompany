from django.db import models
from .base_model import BaseModel


class CommonInfoAboutCompany(BaseModel):
    logo = models.ImageField(upload_to='images/logo')
    video = models.FileField(upload_to='videos/about_company')
    history = models.TextField()
    requestions = models.TextField()

    class Meta:
        verbose_name_plural = 'Информация о компании'

    def __str__(self):
        return f'{self.history}'
