from django.shortcuts import render


def polygon(request):
    return render(request, 'common/polygon.html')
