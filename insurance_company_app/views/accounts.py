from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.http import HttpResponseRedirect


@login_required
def profile(request):
    return render(request, 'account/profile.html')


def register(request):
    if request.method == 'GET':
        return render(request, 'registration/registration.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        user = User.objects.create_user(username, email, password)
        user.groups.add(Group.objects.get(name='User'))
        user.save()
        return HttpResponseRedirect('/')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')
