from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect


@login_required
def index(request):
    return render(request, 'account/index.html')


def register(request):
    if request.method == 'GET':
        return render(request, 'registration/registration.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        user = User.objects.create_user(username, email, password)
        user.save()
        return HttpResponseRedirect('/')
