from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User, Group
from django.http import HttpResponseRedirect
from django.urls import reverse
from .statistics import *
from .insurance_contract import InsuranceContract
from ..models import CompanyBranch, InsuranceType
from ..models.insurance_client import InsuranceClient
from ..forms.authorization import RegistrationForm, LoginForm


def register(request):
    if request.method == 'GET':
        form = RegistrationForm()
        return render(request, 'registration/registration.html', {'form': form})
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            password = request.POST.get('password')
            password_confirm = request.POST.get('password_confirm')
            name = request.POST.get('name')
            surname = request.POST.get('surname')
            second_name = request.POST.get('second_name')
            email = request.POST.get('email')
            age = request.POST.get('age')
            phone_number = request.POST.get('phone_number')
            address = request.POST.get('address')
            login = request.POST.get('login')
            if password_confirm != password:
                form = RegistrationForm(request.POST)
                error = 'Passwords must be equal'
                context = {
                    'form': form,
                    'error': error
                }
                return render(request, 'registration/registration.html', context)

            username = login
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
        else:
            form = RegistrationForm(request.POST)
            return render(request, 'registration/registration.html', {'form': form})
        return HttpResponseRedirect('/home')


def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('login')
        password = request.POST.get('password')
        print(username, password)
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            if user.groups.filter(name='Employee').exists():
                return HttpResponseRedirect(reverse('employee_profile_view'))
            elif user.groups.filter(name='User').exists():
                return HttpResponseRedirect(reverse('user_profile_view'))
        else:
            form = LoginForm(request.POST)
            error = 'User not found'
            context = {
                'form': form,
                'error': error
            }
            return render(request, 'registration/login.html', context)
    else:
        form = LoginForm()
        return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/home')


def superuser_check(user):
    return user.is_superuser


def user_check(user):
    return user.groups.filter(name='User').exists()


def employee_check(user):
    return user.groups.filter(name='Employee').exists()


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


@login_required
@user_passes_test(user_check, login_url='/login/')
def user_profile_view(request):
    user = request.user
    client = InsuranceClient.objects.filter(user=user).first()
    contracts = InsuranceContract.objects.filter(client=client)
    context = {
        'user': user,
        'contracts': contracts
    }
    return render(request, 'account/profile.html', context)


@login_required
@user_passes_test(employee_check, login_url='/login/')
def employee_profile_view(request):
    user = request.user
    agent = InsuranceAgent.objects.filter(user=user).first()
    contracts = InsuranceContract.objects.filter(agent=agent)
    context = {
        'user': agent,
        'contracts': contracts
    }
    return render(request, 'account/employee_profile.html', context)


@login_required
@user_passes_test(superuser_check, login_url='/login/')
def superuser_profile_view(request):
    user = request.user
    company_branches = CompanyBranch.objects.all()
    for branch in company_branches:
        agents = InsuranceAgent.objects.filter(branch_name=branch)
        branch.agents = agents
    contracts = InsuranceContract.objects.all()
    agents = InsuranceAgent.objects.all()
    insurance_types = InsuranceType.objects.all()

    for agent in agents:
        agent_contracts = InsuranceContract.objects.filter(agent=agent)
        agent.salary = sum(contract.agent_salary for contract in agent_contracts)

    context = {
        'user': user,
        'branches': company_branches,
        'contracts': contracts,
        'insurance_types': insurance_types,
        'agents_details': agents
    }
    return render(request, 'account/superuser_profile.html', context)
