from django.db import models

from . import InsuranceType
from .company_branch import CompanyBranch
from .insurance_agent import InsuranceAgent
from .insurance_client import InsuranceClient
from .base_model import BaseModel


class InsuranceContract(BaseModel):
    date = models.DateField()
    insurance_sum = models.FloatField()
    insurance_type = models.ForeignKey(InsuranceType, on_delete=models.CASCADE)
    tariff_rate = models.FloatField()
    branch_name = models.ForeignKey(CompanyBranch, on_delete=models.CASCADE)
    agent = models.ForeignKey(InsuranceAgent, on_delete=models.CASCADE)
    client = models.ForeignKey(InsuranceClient, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Договор'
        verbose_name_plural = 'Договора'

    def __str__(self):
        return f'Contract between {self.agent.surname} - {self.client.surname}'

    @property
    def commission(self):
        return self.insurance_sum * self.tariff_rate

    @property
    def agent_salary(self):
        commission = self.commission
        percentage = self.insurance_type.percentage
        return commission * percentage
