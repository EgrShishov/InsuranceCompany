from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.http import HttpResponseRedirect


@login_required
def profile(request):
    user = request.user
    if user.is_authenticated:
        return render(request, 'account/profile.html', {"user": user})
    else:
        return render(request, 'account/not_authenticated.html')


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


def superuser_check(user):
    return user.is_superuser


@login_required
@user_passes_test(superuser_check, login_url='/login/')
def superuser_extra_view(request):
    data = {

    }
    return render(request, 'common/superuser_statistics.html', data)
