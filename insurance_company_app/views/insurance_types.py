from django.shortcuts import render
from ..models import InsuranceType


def index(request):
    types = InsuranceType.objects.all()
    return render(request, 'insurance/insurance_types.html', {'types': types})
