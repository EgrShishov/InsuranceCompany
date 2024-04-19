from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponseForbidden
from ..models.insurance_agent import CompanyBranch
from ..constants import ErrorMessages, InfoMessages
import logging


def index(request):
    logging.info(InfoMessages.PROCESSING_REQUEST + request.resolver_match.view_name)
    branches = CompanyBranch.objects.all()
    return render(request, "company_branch/index.html", {"branches": branches})


#will be added later
def detail(request):
    pass


@login_required
@permission_required('insurance_company_app.add_companybranch')
def create(request):
    logging.info(InfoMessages.PROCESSING_REQUEST + request.resolver_match.view_name)
    try:
        if request.method == "GET":
            return render(request, "company_branch/create.html")
        if request.method == "POST":
            company_branch = CompanyBranch()
            company_branch.name = request.POST.get("name")
            company_branch.address = request.POST.get("address")
            company_branch.phone_number = request.POST.get("phone_number")
            company_branch.save()
    except Exception as e:
        logging.error(ErrorMessages.PROCCESING_REQUEST_ERROR, e)
    return HttpResponseRedirect("/")


@login_required
@permission_required('insurance_company_app.change_companybranch')
def edit(request, id):
    logging.info(InfoMessages.PROCESSING_REQUEST + request.resolver_match.view_name)
    try:
        company_branch = CompanyBranch.objects.get(id=id)
        if not request.user.has_perm('your_app.change_companybranch', company_branch):
            return HttpResponseForbidden("You don't have permission to edit this company branch.")
        if request.method == "POST":
            company_branch.name = request.POST.get("name")
            company_branch.address = request.POST.get("address")
            company_branch.phone_number = request.POST.get("phone_number")
            company_branch.save()
            return HttpResponseRedirect("/")
        else:
            return render(request, "company_branch/edit.html", {"company_branch": company_branch})
    except Exception as e:
        logging.error(ErrorMessages.CANNOT_FOUND_ITEM, e)
        return HttpResponseNotFound("<h2>Branch not found</h2>")


@login_required
@permission_required('insurance_company_app.delete_companybranch')
def delete(request, id):
    logging.info(InfoMessages.PROCESSING_REQUEST + request.resolver_match.view_name)
    try:
        company_branch = CompanyBranch.objects.get(id=id)
        company_branch.delete()
        return HttpResponseRedirect("/")
    except Exception as e:
        logging.error(ErrorMessages.CANNOT_FOUND_ITEM, e)
        return HttpResponseNotFound("<h2>Branch not found</h2>")
