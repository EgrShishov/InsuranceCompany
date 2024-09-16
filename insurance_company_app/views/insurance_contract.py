import uuid
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponseForbidden
from ..models.insurance_contract import InsuranceContract, InsuranceClient
from ..forms.insurance_contract import InsuranceContractForm
from django.utils import timezone


@login_required(login_url='login')
@permission_required('insurance_company_app.view_insurancecontract')
def index(request):
    client = InsuranceClient.objects.get(user=request.user)
    contracts = client.insurancecontract_set.all()
    return render(request, "insurance_contract/index.html", {"contracts": contracts})


@login_required(login_url='login')
@permission_required('insurance_company_app.add_insurancecontract')
def create(request):
    if request.method == "GET":
        form = InsuranceContractForm()
        context = {
            'form': form,
        }
        return render(request, "insurance_contract/create.html", context)

    if request.method == "POST":
        form = InsuranceContractForm(request.POST)
        if form.is_valid():
            form.save(user=request.user)
        else:
            print("Форма содержит ошибки")

        if 'cart' not in request.session:
            request.session['cart'] = {}

        cart = request.session['cart']

        contract_id = str(uuid.uuid4())
        if contract_id in cart:
            cart[contract_id]['quantity'] += 1
        else:
            cart[contract_id] = {
                'id': contract_id,
                'sum': form.cleaned_data['insurance_sum'],
                'agent': f'{form.cleaned_data["agent"]}',
                'quantity': 1,
                'object': form.cleaned_data["insurance_object"]
            }
            request.session.modified = True
            print('session_cart', cart)

    return HttpResponseRedirect("/contracts/")


@login_required(login_url='login')
@permission_required('insurance_company_app.change_insurancecontract')
def edit(request, id):
    try:
        contract = InsuranceContract.objects.get(id=id)
        if not request.user.has_perm('insurance_company_app.edit_contract', contract):
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


@login_required(login_url='login')
@permission_required('insurance_company_app.delete_insurancecontract')
def delete(request, id):
    try:
        contract = InsuranceContract.objects.get(id=id)
        contract.delete()
        return HttpResponseRedirect("/")
    except contract.DoesNotExist:
        return HttpResponseNotFound("<h2>Contract not found</h2>")
