from django.db import models
from .company_branch import CompanyBranch
from .base_model import BaseModel


class InsuranceContract(BaseModel):
    date = models.DateField()
    insurance_sum = models.FloatField()
    insurance_type = models.TextField()
    tariff_rate = models.FloatField()
    branch_name = models.ForeignKey(CompanyBranch, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Договор'
        verbose_name_plural = 'Договора'

    def __str__(self):
        return self.date
