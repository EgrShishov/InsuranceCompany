from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from ..models import Review


def index(request):
    reviews = Review.objects.all()
    return render(request, 'insurance/reviews.html', {'reviews': reviews})


@login_required
@permission_required
def create(request):
    pass
