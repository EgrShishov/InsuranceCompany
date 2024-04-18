from django.db import models
from .company_branch import CompanyBranch
from .base_model import BaseModel


class InsuranceAgent(BaseModel):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=40)
    second_name = models.CharField(max_length=40)
    age = models.IntegerField()
    address = models.CharField(max_length=80)
    phone_number = models.CharField(max_length=16)
    branch_name = models.ForeignKey(CompanyBranch, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Страховой агент'
        verbose_name_plural = 'Страховые агенты'

    def __str__(self):
        return self.name
