from django.db import models
from django.core.exceptions import ValidationError
from .base_model import BaseModel
from .company_branch import CompanyBranch


class Vacancy(BaseModel):
    position_name = models.CharField(max_length=200)
    salary = models.DecimalField(max_digits=10, decimal_places=5)
    vacancy_description = models.CharField(max_length=300)
    branch = models.ForeignKey(CompanyBranch, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'

    def __str__(self):
        return f'{self.position_name} with salary {self.salary}'

    def clean(self):
        super().clean()

        if self.salary < 0:
            raise ValidationError('Salary cannot be negative')
