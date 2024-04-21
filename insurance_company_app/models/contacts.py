from django.db import models
from .base_model import BaseModel
from .insurance_agent import InsuranceAgent


class Contacts(BaseModel):
    employee_image = models.ImageField()
    agent = models.ForeignKey(InsuranceAgent, on_delete=models.CASCADE)
    position = models.CharField(max_length=200)
    email = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Контакты'

    def __str__(self):
        return f'{self.agent.surname} - {self.position}'

    def get_employee_image_url(self):
        if self.employee_image:
            return self.employee_image.url
        else:
            return 'path/to/default/image' #need to change
