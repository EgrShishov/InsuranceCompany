from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from django.contrib.auth.models import User, Group
from django.http import HttpResponseRedirect
from .statistics import *


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
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        second_name = request.POST.get('second_name')
        email = request.POST.get('email')
        age = request.POST.get('age')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')

        user = User.objects.create_user(username, email, password)
        client = InsuranceClient()
        client.user = user
        client.name = name
        client.second_name = second_name
        client.surname = surname
        client.age = age
        client.phone_number = phone_number
        client.address = address
        client.save()

        user.groups.add(Group.objects.get(name='User'))
        user.save()
        return HttpResponseRedirect('/home')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/home')


def superuser_check(user):
    return user.is_superuser


@login_required
@user_passes_test(superuser_check, login_url='/login/')
def superuser_extra_view(request):
    total_sales = get_total_sales()
    sales_statistics = get_sales_statistics()
    clients_age_statistics = get_clients_age_statistics()
    most_popular_insurance_type = get_most_popular_insurance_type()
    agents = get_agent_statistics()
    chart = visualize_sales_per_agent()
    client_age = visualize_statistics_per_clients_group()

    context = {
        "total_sales": total_sales,
        "sales_statistics": sales_statistics,
        "clients_age_statistics": clients_age_statistics,
        "most_popular_insurance": most_popular_insurance_type,
        "agents": agents,
        "chart_div": chart,
        "client_age_chart": client_age
    }
    return render(request, 'common/superuser_statistics.html', context)
