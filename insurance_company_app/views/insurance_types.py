from django.shortcuts import render
from ..models import InsuranceType


def index(request):
    types = InsuranceType.objects.all()

    search_query = request.GET.get('search')
    if search_query:
        types = types.filter(name__icontains=search_query)

        # Sorting functionality
    sort_by = request.GET.get('sort_by')
    if sort_by == 'name':
        types = types.order_by('name')
    elif sort_by == 'percentage':
        types = types.order_by('percentage')
    elif sort_by == 'name_desc':
        types = types.order_by('-name')
    elif sort_by == 'percentage_desc':
        types = types.order_by('-percentage')

    return render(request, 'insurance/insurance_types.html', {'types': types})
