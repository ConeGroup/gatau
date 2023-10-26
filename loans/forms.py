from django.forms import ModelForm
from loans.models import LoansBook

class LoanForm(ModelForm):
    class Meta:
        model = LoansBook
        fields = ["number_book", "date_return"]