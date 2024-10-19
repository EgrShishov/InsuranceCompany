import json

from ..models.company_branch import CompanyBranch
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseNotFound, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..models.insurance_agent import InsuranceAgent
from django.contrib.auth.models import User, Group


class InsuranceAgentEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, InsuranceAgent):
            return {
                "id": obj.id,
                "name": obj.name,
                "second_name": obj.second_name,
                "surname": obj.surname,
                "age": obj.age,
                "email": obj.address,
                "branch_name": obj.branch_name.name,
                "phone": obj.phone_number,
                "position": obj.job_position,
                "photo": obj.photo.url if obj.photo else None
            }
        return super().default(obj)


def index(request):
    agents = InsuranceAgent.objects.all()
    return render(request, "index.html", {"agents": agents})


@login_required
@permission_required('insurance_company_app.add_insuranceagent')
def create(request):
    if request.method == "POST":
        insurance_agent = InsuranceAgent()
        insurance_agent.name = request.POST.get("name")
        insurance_agent.second_name = request.POST.get("second_name")
        insurance_agent.surname = request.POST.get("surname")
        insurance_agent.age = request.POST.get("age")
        insurance_agent.address = request.POST.get("address")
        insurance_agent.branch_name = request.POST.get("branch_name")
        insurance_agent.phone_number = request.POST.get("phone_number")
        insurance_agent.save()
    return HttpResponseRedirect("/")


@require_http_methods(["POST"])
def create(request):
    try:
        data = json.loads(request.body)
        branch = CompanyBranch.objects.get(name=data.get("branch_name"))
        insurance_agent = InsuranceAgent()
        new_user = User.objects.create_user(
            username=f'{data.get("surname")} {data.get("name")} {data.get("second_name")}',
            email=data.get("email"),
            password='testpassword'
        )

        insurance_agent.user=new_user
        insurance_agent.name=data.get("name")
        insurance_agent.second_name=data.get("second_name")
        insurance_agent.surname=data.get("surname")
        insurance_agent.age=data.get("age")
        insurance_agent.address=data.get("email")
        insurance_agent.branch_name=branch
        insurance_agent.phone_number=data.get("phone_number")
        insurance_agent.job_position=data.get("position")
        insurance_agent.photo=data.get("photo")

        insurance_agent.save()

        group, created = Group.objects.get_or_create(name='Employee')
        insurance_agent.user.groups.add(group)

        message = json.dumps(insurance_agent, cls=InsuranceAgentEncoder)
        return JsonResponse({'status': 'success', 'message': message})
    except CompanyBranch.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Branch not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@login_required
@permission_required('insurance_company_app.change_insuranceagent')
def edit(request, id):
    try:
        insurance_agent = InsuranceAgent.objects.get(id=id)

        if request.method == "POST":
            insurance_agent.name = request.POST.get("name")
            insurance_agent.second_name = request.POST.get("second_name")
            insurance_agent.surname = request.POST.get("surname")
            insurance_agent.age = request.POST.get("age")
            insurance_agent.address = request.POST.get("address")
            insurance_agent.branch_name = request.POST.get("branch_name")
            insurance_agent.phone_number = request.POST.get("phone_number")
            insurance_agent.save()
            return HttpResponseRedirect("/")
        else:
            return render(request, "edit.html", {"insurance_agent": insurance_agent})
    except insurance_agent.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")


@login_required
@permission_required('insurance_company_app.delete_insuranceagent')
def delete(request, id):
    try:
        insurance_agent = InsuranceAgent.objects.get(id=id)
        insurance_agent.delete()
        return HttpResponseRedirect("/")
    except InsuranceAgent.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")
