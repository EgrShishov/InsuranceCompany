from django.shortcuts import render
from ..models import InsuranceAgent


def index(request):
    employees = InsuranceAgent.objects.all()
    context = {
        'employees': employees
    }
    return render(request, 'insurance/contacts.html', context)
