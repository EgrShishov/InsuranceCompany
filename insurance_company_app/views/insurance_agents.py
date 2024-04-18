from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseNotFound
from ..models.insurance_agent import InsuranceAgent


def index(request):
    agents = InsuranceAgent.objects.all()
    return render(request, "index.html", {"agents": agents})


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


def delete(request, id):
    try:
        insurance_agent = InsuranceAgent.objects.get(id=id)
        insurance_agent.delete()
        return HttpResponseRedirect("/")
    except InsuranceAgent.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")
