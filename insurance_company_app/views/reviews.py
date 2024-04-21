from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from ..models import Review
from ..forms.make_review import MakeReview


def index(request):
    reviews = Review.objects.all()
    return render(request, 'insurance/reviews.html', {'reviews': reviews})


@login_required
def create(request):
    if request.method == 'GET':
        context = {
            'form': MakeReview()
        }
        return render(request, 'insurance/make_review.html', context)
    elif request.method == 'POST':
        form = MakeReview(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
        return HttpResponseRedirect('/home')
