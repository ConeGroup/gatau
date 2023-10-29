from django.forms import ModelForm
from reviews.models import Review
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm
from django import forms


class ReviewForm(ModelForm): 
    rating = forms.FloatField(widget=forms.TextInput(attrs={'class':'form-control'}))
    book_review_desc = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    is_recommended = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class':'form-check-input'}))

    class Meta:
        model = Review
        fields = ["rating", "book_review_desc", "is_recommended"]
    
    def custom_error_display(self):
        error_string = ""
        for field, errors in self.errors.items():
            error_string += errors
        return error_string