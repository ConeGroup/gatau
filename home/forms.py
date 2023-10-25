from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm): 
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta: 
        model = User 
        fields = ['username', 'email', 'password1', 'password2',]
    
    def custom_error_display(self):
        error_string = ""
        for field, errors in self.errors.items():
            error_string += errors
        return error_string