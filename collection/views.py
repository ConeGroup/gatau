from django.shortcuts import render, redirect, get_object_or_404
from .models import Collection
from .forms import CollectionForm
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from book.models import Book 
from django.core import serializers


@login_required(login_url='/login')
def collection_list(request):
    collections = Collection.objects.filter(user=request.user)
    context = {
        'name': request.user.username,
        'collections': collections,
    }
    return render(request, 'collection_list.html', context)

# View untuk menambahkan buku ke koleksi menggunakan AJAX
@csrf_exempt
def add_book_to_collection_ajax(request):
    if request.method == 'POST':
        collection_id = request.POST.get('collection_id')
        book_id = request.POST.get('book_id')
        try:
            collection = Collection.objects.get(pk=collection_id, user=request.user)
            book = Book.objects.get(pk=book_id)
            collection.books.add(book)
            return JsonResponse({'status': 'success'})
        except (Collection.DoesNotExist, Book.DoesNotExist):
            return JsonResponse({'status': 'error'})
    return JsonResponse({'status': 'error'})

# View untuk membuat koleksi baru menggunakan AJAX
@csrf_exempt
def create_collection_ajax(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        new_collection = Collection(name=name, user=request.user)
        new_collection.save()
        return JsonResponse({'status': 'success', 'collection_id': new_collection.id})
    return JsonResponse({'status': 'error'})

def edit_collection(request, collection_id):
    collection = get_object_or_404(Collection, pk=collection_id, user=request.user)
    if request.method == 'POST':
        form = CollectionForm(request.POST, instance=collection)
        if form.is_valid():
            form.save()
            return redirect('collection_list')
    else:
        form = CollectionForm(instance=collection)
    return render(request, 'edit_collection.html', {'form': form, 'collection': collection})

def delete_collection(request, collection_id):
    collection = get_object_or_404(Collection, pk=collection_id, user=request.user)
    if request.method == 'DELETE':
        collection.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

def get_collections_json(request):
    collection_item = Collection.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize('json', collection_item))

def get_book_json(request):
    books = Book.objects.all()
    return HttpResponse(serializers.serialize('json', books))