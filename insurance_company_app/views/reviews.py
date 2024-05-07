from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from ..models import Review, InsuranceClient
from ..forms.make_review import MakeReview


def index(request):
    reviews = Review.objects.all()
    return render(request, 'insurance/reviews.html', {'reviews': reviews})


@login_required(login_url='/login')
def create_review(request):
    if request.method == 'POST':
        form = MakeReview(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            insurance_client = InsuranceClient.objects.get(user=request.user)
            review.author = insurance_client
            review.save()
        return HttpResponseRedirect('/home')
    else:
        form = MakeReview()
    context = {
        'form': form
    }
    return render(request, 'insurance/make_review.html', context)
