from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from ..models import Review


class MakeReview(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].label = 'Enter text'

        self.fields['rating'].label = 'Rate our service'
        self.fields['rating'].validators = [MinValueValidator(0), MaxValueValidator(10)]
