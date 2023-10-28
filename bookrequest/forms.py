from django import forms
from django.forms import ModelForm
from bookrequest.models import BookReq
from django.contrib.auth.models import User

class BookReqForm(ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    author = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    isbn = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    year = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    publisher = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    initial_review = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    image_m = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    
    class Meta:
        model = BookReq
        fields = ("title", "author", "isbn", "year", "publisher", "initial_review", "image_m")