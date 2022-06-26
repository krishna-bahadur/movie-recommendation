from dataclasses import field
from django import forms
from .models import Movie, Review


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'budget', 'genres']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review']

class UploadFrom(forms.Form):
    file = forms.FileField()

