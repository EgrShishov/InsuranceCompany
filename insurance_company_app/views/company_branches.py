from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseNotFound
from ..models.insurance_agent import CompanyBranch


def index(request):
    branches = CompanyBranch.objects.all()
    return render(request, "details.html", {"branches": branches})


def create(request):
    if request.method == "POST":
        company_branch = CompanyBranch()
        company_branch.name = request.POST.get("name")
        company_branch.address = request.POST.get("address")
        company_branch.phone_number = request.POST.get("phone_number")
        company_branch.save()
    return HttpResponseRedirect("/")


def edit(request, id):
    try:
        company_branch = CompanyBranch.objects.get(id=id)

        if request.method == "POST":
            company_branch.name = request.POST.get("name")
            company_branch.address = request.POST.get("address")
            company_branch.phone_number = request.POST.get("phone_number")
            company_branch.save()
            return HttpResponseRedirect("/")
        else:
            return render(request, "edit.html", {"insurance_agent": company_branch})
    except company_branch.DoesNotExist:
        return HttpResponseNotFound("<h2>Branch not found</h2>")


def delete(request, id):
    try:
        company_branch = CompanyBranch.objects.get(id=id)
        company_branch.delete()
        return HttpResponseRedirect("/")
    except company_branch.DoesNotExist:
        return HttpResponseNotFound("<h2>Branch not found</h2>")
