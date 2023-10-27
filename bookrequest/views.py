import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from bookrequest.forms import BookReqForm
from bookrequest.models import BookReq
from django.urls import reverse
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

# Create your views here.

@login_required(login_url='../login')
def show_request_page(request):
    book_req = BookReq.objects.filter(user=request.user)

    context = {
        'my_app': 'Marpellus Cenep',
        'name': request.user.username,
        'class': 'PBP C',
        # 'last_login': request.COOKIES['last_login']
    }

    return render(request, "request-page.html", context)

def get_request_item_json(request):
    request_item = BookReq.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize('json', request_item))

@csrf_exempt
def create_request(request):
    if request.method == 'POST':
        title = request.POST.get("title")
        author = request.POST.get("author")
        year = request.POST.get("year")
        publisher = request.POST.get("publisher")
        initial_review = request.POST.get("initial_review")
        image = request.POST.get("image_m")
        user = request.user

        new_request = BookReq(title=title, author=author, year=year, publisher=publisher, initial_review=initial_review, image_m=image, user=user)
        new_request.save()

        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()

@csrf_exempt
def remove_request(request, id):
    try:
        request_item = BookReq.objects.get(pk=id)
        request_item.delete()
        return JsonResponse({'message': 'Request item removed successfully'})
    except BookReq.DoesNotExist:
        return JsonResponse({'message': 'Request item not found'}, status=404)
    
@csrf_exempt
def update_request(request, id):
    request_item = get_object_or_404(BookReq, pk=id)

    if request.method == 'POST':
        request_item.title = request.POST.get("title")
        request_item.author = request.POST.get("author")
        request_item.year = request.POST.get("year")
        request_item.publisher = request.POST.get("publisher")
        request_item.initial_review = request.POST.get("initial_review")
        request_item.image_m = request.POST.get("image_m")
        request_item.user = request.user

        request_item.save()

        return HttpResponse(b"UPDATED", status=201)

    return HttpResponseNotFound()
    