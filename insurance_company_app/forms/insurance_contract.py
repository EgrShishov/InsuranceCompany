from django.core.exceptions import ValidationError
from django.utils import timezone
from django import forms
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from ..models import InsuranceContract, InsuranceType, InsuranceAgent, CompanyBranch, InsuranceObject, Promocode
from ..models.insurance_contract import InsuranceClient


class InsuranceContractForm(forms.Form):
    # def validate_date_not_in_future(self, date):
    #     if date > timezone.now().date():
    #         raise ValidationError('Date cannot be in the future.')

    # def checkIfAgentIsCorrespondingToBranch(self, agent):
    #     branch = CompanyBranch.objects.get(name=agent.branch_name)
    #     print(branch)
    #     if not branch:
    #         raise ValidationError('This agent from other branch')

    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Contract Date'
    )
    insurance_sum = forms.FloatField(
        label='Insurance Sum',
        validators=[MinValueValidator(0, 'Insurance sum cannot be negative.')]
    )
    insurance_type = forms.ChoiceField(
        label='Insurance Type',
        choices=[],  # We'll populate this in the constructor
        widget=forms.Select()
    )
    tariff_rate = forms.FloatField(
        label='Tariff Rate',
        validators=[MinValueValidator(0, 'Insurance tariff cannot be negative.')]
    )
    insurance_object = forms.ChoiceField(
        label='Object',
        choices=[],  # Will populate later
        required=False
    )
    branch_name = forms.ChoiceField(
        label='Company Branch',
        choices=[],  # Will populate later
    )
    agent = forms.ChoiceField(
        label='Insurance Agent',
        choices=[],  # Will populate later
    )
    # def clean_promocode(self):
    #     promocode = self.cleaned_data.get('promocode')
    #     if promocode:
    #         try:
    #             promo_code_obj = Promocode.objects.get(code=promocode)
    #             if not promo_code_obj.is_active:
    #                 raise ValidationError('Promo code is inactive')
    #             if promo_code_obj.expiration_date < timezone.now().date():
    #                 raise ValidationError('Promo code has expired')
    #         except Promocode.DoesNotExist:
    #             raise ValidationError('Invalid promo code')
    #
    #         return promo_code_obj
    #     return None

    # def apply_promocode_discount(self, promo_code_obj, insurance_sum):
    #     if promo_code_obj:
    #         discount_value = promo_code_obj.discount
    #         promo_code_obj.usage_count += 1
    #         return insurance_sum - discount_value
    #     return insurance_sum
    #
    # def clean(self):
    #     cleaned_data = super().clean()
    #
    #     insurance_sum = cleaned_data.get('insurance_sum')
    #     promo_code_obj = cleaned_data.get('promocode')
    #
    #     if insurance_sum and promo_code_obj:
    #         discounted_sum = self.apply_promocode_discount(promo_code_obj, insurance_sum)
    #         cleaned_data['insurance_sum'] = discounted_sum
    #
    #     return cleaned_data

    def __init__(self, *args, **kwargs):
        super(InsuranceContractForm, self).__init__(*args, **kwargs)

        # Populate insurance type choices
        self.fields['insurance_type'].choices = [
            (type.id, f'{type.name}') for type in InsuranceType.objects.all()
        ]

        # Get all insurance objects for selection
        insurance_objects = InsuranceObject.objects.all()
        if insurance_objects:
            self.fields['insurance_object'].choices = [
                (insurance_object.id, f'{insurance_object.name}') for insurance_object in insurance_objects
            ]
        else:
            self.fields['insurance_object'].widget = forms.TextInput()

        # Populate branches
        self.fields['branch_name'].choices = [
            (branch.id, f'{branch.name}, {branch.address}') for branch in CompanyBranch.objects.all()
        ]

        # Populate agents
        self.fields['agent'].choices = [
            (agent.id, f'{agent.surname} {agent.name} {agent.second_name}')
            for agent in InsuranceAgent.objects.all()
        ]

    def clean_promocode(self):
        promocode = self.cleaned_data.get('promocode')
        if promocode:
            try:
                promo_code_obj = Promocode.objects.get(code=promocode)
                if not promo_code_obj.is_active:
                    raise ValidationError('Promo code is inactive')
                if promo_code_obj.expiration_date < timezone.now().date():
                    raise ValidationError('Promo code has expired')
            except Promocode.DoesNotExist:
                raise ValidationError('Invalid promo code')
            return promo_code_obj
        return None

    def apply_promocode_discount(self, promo_code_obj, insurance_sum):
        if promo_code_obj:
            discount_value = promo_code_obj.discount
            promo_code_obj.usage_count += 1
            promo_code_obj.save()
            return insurance_sum - discount_value
        return insurance_sum

    def clean(self):
        cleaned_data = super().clean()

        insurance_sum = cleaned_data.get('insurance_sum')
        promo_code_obj = self.clean_promocode()

        if insurance_sum and promo_code_obj:
            discounted_sum = self.apply_promocode_discount(promo_code_obj, insurance_sum)
            cleaned_data['insurance_sum'] = discounted_sum

        return cleaned_data

    def save(self, commit=True, user=None):
        insurance_contract = InsuranceContract(
            date=self.cleaned_data['date'],
            insurance_sum=self.cleaned_data['insurance_sum'],
            insurance_type=InsuranceType.objects.get(id=self.cleaned_data['insurance_type']),
            tariff_rate=self.cleaned_data['tariff_rate'],
            branch_name=CompanyBranch.objects.get(id=self.cleaned_data['branch_name']),
            insurance_object=InsuranceObject.objects.get(id=self.cleaned_data['insurance_object']),
            agent=InsuranceAgent.objects.get(id=self.cleaned_data['agent']),
            client=InsuranceClient.objects.get(user=user)
        )

        if commit:
            insurance_contract.save()
        return insurance_contract
