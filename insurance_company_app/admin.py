from django.contrib import admin
from .models.company_branch import CompanyBranch
from .models.insurance_agent import InsuranceAgent
from .models.insurance_contract import InsuranceContract
from .models.insurance_object import InsuranceObject
from .models.insurance_client import InsuranceClient
from .models.insurance_type import InsuranceType
from .models.review import Review
from .models.promocode import Promocode


@admin.register(CompanyBranch)
class CompanyBranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone_number')
    list_filter = ('name', 'address', 'phone_number')
    #list_editable = ('name', 'address', 'phone_number')


@admin.register(InsuranceType)
class InsuranceTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_description')
    list_filter = ('name',)
    #list_editable = ('name', 'description')

    def get_description(self, obj):
        return obj.description


@admin.register(InsuranceClient)
class InsuranceClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'second_name', 'address', 'phone_number', 'age')
    list_filter = ('surname', 'age', 'address')
    list_display_links = ('surname', )
    list_editable = ('name', 'address', 'phone_number', 'age', 'second_name')


@admin.register(InsuranceObject)
class InsuranceObjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_filter = ('name', 'description')
    list_display_links = ('name', )
    list_editable = ('description', )


@admin.register(InsuranceAgent)
class InsuranceAgentAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'second_name', 'age', 'address', 'phone_number', 'branch_name')
    list_filter = ('name', 'surname', 'second_name', 'age', 'address', 'phone_number', 'branch_name')
    list_display_links = ('name', )
    list_editable = ('surname', 'second_name', 'age', 'address', 'phone_number', 'branch_name')


@admin.register(InsuranceContract)
class InsuranceContractAdmin(admin.ModelAdmin):
    list_display = ('date', 'insurance_type', 'insurance_sum', 'tariff_rate', 'branch_name')
    list_filter = ('date', 'insurance_type', 'insurance_sum', 'tariff_rate', 'branch_name')
    list_editable = ('insurance_type', 'insurance_sum', 'tariff_rate', 'branch_name')
    list_display_links = ('date', )


@admin.register(Promocode)
class PromocodeAdmin(admin.ModelAdmin):
    list_display = ('name','discount', 'is_active', 'expiration_date', 'get_usages')
    list_filter = ('name','discount', 'is_active', 'expiration_date')
    list_display_links = ('name',)
    list_editable = ('discount', 'is_active', 'expiration_date')

    def get_usages(self, obj):
        return obj.usage_count


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('text','author', 'rating')
    list_filter = ('text','author', 'rating')
    list_display_links = ('text',)
