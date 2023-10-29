from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Collection
from .forms import CollectionForm
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from book.models import Book 
from django.core import serializers


@login_required(login_url='/login')
def show_collection(request):
    collections = Collection.objects.filter(user=request.user)
    books = Book.objects.all()  # Ambil semua buku
    context = {
        'name': request.user.username,
        'collections': collections,
        'books': books,  # Tambahkan buku ke dalam konteks
    }
    return render(request, 'collection_list.html', context)

def get_collection_json(request):
    collections = Collection.objects.filter(user=request.user)
    collection_data = []

    for collection in collections:
        books_data = list(collection.books.values('title', 'author', 'image_l'))  # Menambahkan 'image_s' ke values
        collection_info = {
            'id': collection.id,
            'name': collection.name,
            'books': books_data,  # Menggunakan books_data yang sudah mencakup 'image_s'
        }
        collection_data.append(collection_info)

    return JsonResponse(collection_data, safe=False)

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
            return HttpResponse(b"CREATED", status=201)
        except (Collection.DoesNotExist, Book.DoesNotExist):
            return HttpResponseNotFound()
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


# View untuk membuat koleksi baru menggunakan AJAX
@csrf_exempt
def create_collection_ajax(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        user = request.user

        new_collection = Collection(name=name, user=user)
        new_collection.save()

        return HttpResponse(b"CREATED", status=201)
    return HttpResponseNotFound()


@login_required(login_url='/login')
def edit_collection(request, collection_id):
    collection = get_object_or_404(Collection, pk=collection_id, user=request.user)
    books = Book.objects.all()  # Ambil semua buku

    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        book = get_object_or_404(Book, pk=book_id)
        collection.books.add(book)  # Tambahkan buku ke dalam koleksi
        return redirect('collection:edit_collection', collection_id=collection.id)

    context = {
        'collection': collection,
        'books': books,
    }

    return render(request, 'edit_collection.html', context)

@login_required(login_url='/login')
def add_book_to_collection(request, collection_id):
    if request.method == 'POST':
        collection = get_object_or_404(Collection, pk=collection_id, user=request.user)
        book_id = request.POST.get('book_id')
        book = get_object_or_404(Book, pk=book_id)
        collection.books.add(book)
        return redirect('collection:edit_collection', collection_id=collection.id)
    return JsonResponse({'status': 'error'})

@login_required(login_url='/login')
def remove_book_from_collection(request, collection_id, book_id):
    if request.method == 'GET':
        collection = get_object_or_404(Collection, pk=collection_id, user=request.user)
        book = get_object_or_404(Book, pk=book_id)
        collection.books.remove(book)
        return redirect('collection:edit_collection', collection_id=collection.id)
    return JsonResponse({'status': 'error'})

def delete_collection(request, collection_id):
    if request.method == 'DELETE':
        try:
            collection = Collection.objects.get(pk=collection_id, user=request.user)
            collection.delete()
            return JsonResponse({'status': 'success', 'message': 'Collection deleted successfully'})
        except Collection.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Collection not found'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def get_book_json(request):
    books = Book.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize('json', books))

def show_json(request):
    data = Collection.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_json_by_id(request, id):
    data = Collection.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
