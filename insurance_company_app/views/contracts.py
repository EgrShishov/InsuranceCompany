from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseNotFound
from ..models.insurance_contract import InsuranceContract


# сохранение данных в бд
def create(request):
    if request.method == "POST":
        contract = InsuranceContract()
        contract.insurance_type = request.POST.get("type")
        contract.branch_name = request.POST.get("branch_name")
        contract.date = request.POST.get("date")
        contract.insurance_sum = request.POST.get("sum")
        contract.tariff_rate = request.POST.get("tariff")
        contract.save()
    return HttpResponseRedirect("/")


# изменение данных в бд
def edit(request, id):
    try:
        contract = InsuranceContract.objects.get(id=id)

        if request.method == "POST":
            contract.insurance_type = request.POST.get("type")
            contract.branch_name = request.POST.get("branch_name")
            contract.date = request.POST.get("date")
            contract.insurance_sum = request.POST.get("sum")
            contract.tariff_rate = request.POST.get("tariff")
            contract.save()
            return HttpResponseRedirect("/")
        else:
            return render(request, "edit.html", {"contract": contract})
    except contract.DoesNotExist:
        return HttpResponseNotFound("<h2>Contract not found</h2>")


# удаление данных из бд
def delete(request, id):
    try:
        contract = InsuranceContract.objects.get(id=id)
        contract.delete()
        return HttpResponseRedirect("/")
    except contract.DoesNotExist:
        return HttpResponseNotFound("<h2>Contract not found</h2>")
