from django.shortcuts import render
from ..models.about_company import CommonInfoAboutCompany


def index(request):
    aboutCompany = CommonInfoAboutCompany.objects.first()
    context = {
        'logo': aboutCompany.logo,
        'video': aboutCompany.video,
        'history': aboutCompany.history,
        'requestions': aboutCompany.requestions
    }
    return render(request, 'insurance/about.html', context)