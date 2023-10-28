from django import forms
from loans.models import LoansBook

class LoanForm(forms.ModelForm):
    class Meta:
        model = LoansBook
        fields = ["number_book", "date_return"]

        widgets = {
            'number_book': forms.NumberInput(attrs={'class': 'form-control'}),
            'date_return': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'min': '{{ today }}', 'max': '{{ maxDate }}'}),
        }