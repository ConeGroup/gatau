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
        'items': items,
    }

    return render(request, "loans.html", context)

def get_product_json(request):
    product_item = LoansBook.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize('json', product_item))

@csrf_exempt
def add_book_ajax(request):
    if request.method == 'POST':
        number_book = request.POST.get("number_book")
        date_return = request.POST.get("date_return")
        user = request.user

        new_product = LoansBook(number_book=number_book, date_return=date_return, user=user)
        new_product.save()

        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()

def delete_book(request, book_id):
    if request.method == 'DELETE':
        LoansBook.objects.filter(id=book_id).delete()

        return JsonResponse({'status':'success'})

def get_book_json(request):
    books = Book.objects.all()
    return HttpResponse(serializers.serialize('json', books))

def show_loans_page(request):
    return HttpResponseRedirect(reverse('show_loans'))
