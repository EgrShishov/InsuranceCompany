from django.shortcuts import render
from ..models import FAQ


def index(request):
    faqs = FAQ.objects.all()
    context = {
        'faqs': faqs
    }
    return render(request, 'insurance/faq.html', context)
