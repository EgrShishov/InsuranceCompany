from django.shortcuts import render


def privacy_policy(request):
    return render(request, 'insurance/privacy_policy.html')
