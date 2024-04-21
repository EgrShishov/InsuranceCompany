from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from ..models import InsuranceClient, Review


class MakeReview(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'author', 'rating']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['text'].label = 'Enter text'
        self.fields['rating'].label = 'Rate our service'


class CreateReviewView(LoginRequiredMixin, CreateView):
    template_name = 'insurance/make_review.html'
    form_class = MakeReview
    success_url = '/home'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
