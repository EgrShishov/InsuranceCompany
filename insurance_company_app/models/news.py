from django.db import models
from .base_model import BaseModel
from .insurance_agent import InsuranceAgent


class News(BaseModel):
    title = models.CharField(max_length=200)
    text = models.TextField()
    publish_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/news')

    author = models.ForeignKey(InsuranceAgent, on_delete=models.SET_DEFAULT, default=None)

    class Meta:
        verbose_name_plural = 'Новости'

    def __str__(self):
        return f'{self.title} - {self.text} - {self.author.surname}'
