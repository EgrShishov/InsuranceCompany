from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponseForbidden
from ..models.insurance_contract import InsuranceContract
from django.utils import timezone


@login_required
@permission_required('insurance_company_app.view_insurancecontract')
def index(request):
    contracts = InsuranceContract.objects.all()
    return render(request, "insurance_contract/index.html", {"contracts": contracts})


@login_required
@permission_required('insurance_company_app.add_insurancecontract')
def create(request):
    if request.method == "GET":
        return render(request, "insurance_contract/create.html")
    if request.method == "POST":
        contract = InsuranceContract()
        contract.date = timezone.now()
        contract.branch_name = request.POST.get("branch_name")
        contract.insurance_type = request.POST.get("insurance_type")
        contract.tariff_rate = request.POST.get("tariff_rate")
        contract.insurance_sum = request.POST.get("sum")
        contract.save()
    return HttpResponseRedirect("/")


@login_required
@permission_required('insurance_company_app.change_insurancecontract')
def edit(request, id):
    try:
        contract = InsuranceContract.objects.get(id=id)
        if not request.user.has_perm('your_app.edit_contract', contract):
            return HttpResponseForbidden("You don't have permission to edit this contract.")
        if request.method == "POST":
            contract.date = timezone.now()
            contract.branch_name = request.POST.get("branch_name")
            contract.insurance_type = request.POST.get("insurance_type")
            contract.tariff_rate = request.POST.get("tariff_rate")
            contract.insurance_sum = request.POST.get("sum")
            contract.save()
            return HttpResponseRedirect("/")
        else:
            return render(request, "insurance_contract/edit.html", {"insurance_contract": contract})
    except contract.DoesNotExist:
        return HttpResponseNotFound("<h2>Contract not found</h2>")


@login_required
@permission_required('insurance_company_app.delete_insurancecontract')
def delete(request, id):
    try:
        contract = InsuranceContract.objects.get(id=id)
        contract.delete()
        return HttpResponseRedirect("/")
    except contract.DoesNotExist:
        return HttpResponseNotFound("<h2>Contract not found</h2>")
