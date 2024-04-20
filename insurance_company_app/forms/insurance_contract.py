import logging

from django import forms
from ..models import InsuranceContract, InsuranceType, InsuranceAgent, CompanyBranch


class InsuranceContractForm(forms.ModelForm):
    class Meta:
        model = InsuranceContract
        fields = ['date', 'insurance_sum', 'insurance_type', 'branch_name', 'agent']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].widget.attrs['class'] = 'datepicker'
        self.fields['date'].label = 'Contract Date'

        self.fields['insurance_type'].widget = forms.Select(choices=[(type.id, f'{type.name}') for type in InsuranceType.objects.all()])
        self.fields['insurance_type'].label = 'Insurance type'

        self.fields['insurance_sum'].label = 'Insurance Sum'

        self.fields['branch_name'].label = 'Company branch'
        self.fields['branch_name'].widget = forms.Select(
            choices=[(branch.id, f'{branch.name}, {branch.address}') for branch in CompanyBranch.objects.all()])

        self.fields['agent'].queryset = InsuranceAgent.objects.all()
        self.fields['agent'].widget = forms.Select(
            choices=[(agent.id, f'{agent.surname} {agent.name} {agent.second_name}') for agent in InsuranceAgent.objects.all()])
        self.fields['agent'].label = 'Insurance agent'
