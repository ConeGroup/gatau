from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from loans.forms import LoanForm
from loans.models import LoansBook
from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages  
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from book.models import Book


# Create your views here.
@login_required(login_url='/login')
def show_loans(request):
    items = LoansBook.objects.filter(user=request.user)
    context = {
        'name': request.user.username,
        'class': 'PBP C',
        'items': items,
    }

    return render(request, "loans.html", context)

def get_product_json(request):
    product_item = LoansBook.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize('json', product_item))

@csrf_exempt
def add_book_ajax(request):
    if request.method == 'POST':
        form = LoanForm(request.POST)
        if form.is_valid():
            new_loan = form.save(commit=False)  # Mencegah penyimpanan langsung ke database
            new_loan.user = request.user  # Atur user sesuai dengan pengguna yang masuk
            new_loan.save()  # Simpan ke database
            return JsonResponse({'message': 'CREATED'}, status=201)
        else:
            return JsonResponse({'message': 'Invalid Form Data'}, status=400)

    return HttpResponseNotFound()

def delete_book(request, book_id):
    if request.method == 'DELETE':
        LoansBook.objects.filter(id=book_id).delete()

        return JsonResponse({'status':'success'})

def get_book_json(request):
    books = Book.objects.all()
    return HttpResponse(serializers.serialize('json', books))