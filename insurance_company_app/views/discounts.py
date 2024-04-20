from django.shortcuts import render
from ..models import Promocode


def index(request):
    promocodes = Promocode.objects.all()
    return render(request, 'insurance/discounts.html', {'promocodes': promocodes})
