from django.contrib import admin
from .models.company_branch import CompanyBranch
from .models.insurance_agent import InsuranceAgent
from .models.insurance_contract import InsuranceContract
from .models.insurance_object import InsuranceObject
from .models.insurance_client import InsuranceClient
from .models.insurance_type import InsuranceType


# Register your models here.
admin.site.register(CompanyBranch)
admin.site.register(InsuranceType)
admin.site.register(InsuranceClient)
admin.site.register(InsuranceObject)
admin.site.register(InsuranceAgent)
admin.site.register(InsuranceContract)
