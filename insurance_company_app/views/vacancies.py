from django.shortcuts import render
from ..models.vacancy import Vacancy


def index(request):
    vacancies = Vacancy.objects.all()
    context = {
        'vacancies': vacancies
    }
    return render(request, 'insurance/vacancies.html', context)
