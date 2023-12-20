import json
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.core import serializers
from book.models import Book
from reviews.models import Review
from reviews.forms import ReviewForm
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User



@login_required(login_url='../login')
def show_main(request):
    books = Book.objects.all()
    reviews = Review.objects.all()
    this_user_reviews = Review.objects.filter(user=request.user)
    total_reviews = Review.objects.filter(user=request.user).count()

    context = {
        'user' : request.user,
        'books' : books,
        'reviews' : reviews,
        'this_user_reviews' : this_user_reviews,
        'total_reviews' : total_reviews,
    }
    return render(request, "main.html", context)

def review_page(request):
    books = Book.objects.all()
    reviews = Review.objects.all()
    form = ReviewForm()
    context = {
        'user' : request.user,
        'books' : books,
        'reviews' : reviews,
        'form' : form,
    }
    return render(request, "review_page.html", context)

def book_details(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    reviews = Review.objects.filter(book_id = book_id)
    context = {
        'user' : request.user,
        'book' : book,
        'reviews' : reviews,
    }
    return render(request, "book_details.html", context)


def get_book_by_id_json(request, id):
    book = Book.objects.get(pk=id)
    book_data = {
        'title': book.title,
        'author': book.author,
        'year': book.year,
        'publisher': book.publisher,
        'image_m': book.image_m,
        'image_l': book.image_l,
    }
    return JsonResponse(book_data)

def get_review_by_id_json(request, id):
    review = get_object_or_404(Review, pk=id)
    review_data = {
        'book': review.book,
        'user': request.user,
        'book_review_desc': review.book_review_desc,
        'rating': review.rating,
        'is_recommended': review.is_recommended,
    }
    return JsonResponse(review_data)

def update_review(request, review_id):
    try:
        review = Review.objects.get(pk=review_id)
        review.rating = request.POST['rating']
        review.book_review_desc = request.POST['book_review_desc']
        review.is_recommended = request.POST['is_recommended']
        review.save()
        return JsonResponse({'message': 'Review updated successfully'})
    except Review.DoesNotExist:
        return JsonResponse({'error': 'Review not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def get_review_by_user_json(request):
    user = request.user
    reviews = Review.objects.filter(user=user)
    review_data = []

    for review in reviews:
        review_data.append({
            'id' : review.id,
            'book_id': review.book.id,
            'book_title': review.book.title,  # Include the book title
            'rating': review.rating,
            'book_review_desc': review.book_review_desc,
            'is_recommended': review.is_recommended,
            'date_added': review.date_added,
        })

    return JsonResponse({'reviews': review_data})

def get_book_json(request):
    books = Book.objects.all()
    return HttpResponse(serializers.serialize('json', books))

def get_book_user(request):
    user_reviewed_books = Review.objects.filter(user=request.user).values_list('book', flat=True)
    books = Book.objects.exclude(pk__in=user_reviewed_books)

    return HttpResponse(serializers.serialize('json', books))

def get_review_json(request):
    reviews = Review.objects.all()
    return HttpResponse(serializers.serialize('json', reviews))

def back_to_main(request):
    return HttpResponseRedirect(reverse('reviews:show_main'))

@csrf_exempt
def add_review_ajax(request):
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        book_id = request.POST.get('book_id')
        book_review_desc = request.POST.get('book_review_desc')
        is_recommended = request.POST.get('is_recommended')
        if is_recommended == 'yes':
            is_recommended = True
        else:
            is_recommended = False

        book = Book.objects.get(pk = book_id)

        review = Review(
            user=request.user,
            book=book, 
            rating=rating,
            book_review_desc=book_review_desc,
            is_recommended=bool(is_recommended)
        )
        review.save()

        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()

def review_sheet(request, id):
    form = ReviewForm()
    book = get_object_or_404(Book, pk=id)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse('reviews:show_main'))
            
    context = {
        'form':form,
        'book':book,
    }
    return render(request, 'review_sheet.html', context)

@csrf_exempt
def delete_review(request, id):
    try:
        review = Review.objects.get(pk=id)
        review.delete()
        return JsonResponse({'message': 'Review deleted successfully'})
    except Review.DoesNotExist:
        return JsonResponse({'message': 'Review item not found'}, status=404)
    
@csrf_exempt
def edit_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    form = ReviewForm(request.POST or None, instance=review)

    if request.method == 'POST':
        review.rating = request.POST.get("edit_rating")
        review.book_review_desc = request.POST.get("edit_desc")
        is_recommended = request.POST.get('edit_is_recommended')
        if is_recommended == 'yes':
            is_recommended = True
        else:
            is_recommended = False
        review.is_recommended = bool(is_recommended)
        review.user = request.user
        review.save()


        return HttpResponse(b"UPDATED", status=201)

    return HttpResponseNotFound()

# @csrf_exempt
# def edit_review(request, review_id):
#     review = get_object_or_404(Review, pk=review_id)
#     form = ReviewForm(request.POST or None, instance=review)


#     if form.is_valid() and request.method == "POST":
#         # Simpan form dan kembali ke halaman awal
#         form.save()
#         return HttpResponseRedirect(reverse('reviews:show_main'))

#     context = {'form': form}
#     print("hello")
#     return render(request, "review_sheets.html", context)



def add_review_form(request):
    form = ReviewForm(request.POST or None)
    book_id = request.POST.get('book_id')
    book = Book.objects.get(pk = book_id)
    print(book_id)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.book = book
            review.save()
            messages.success(request, 'Your review has been successfully created!')
            return redirect('reviews:show_main')
            
    context = {'form':form}
    return render(request, 'create_review.html', context)

@csrf_exempt
def create_review_flutter(request):
    if request.method == 'POST':
        
        data = json.loads(request.body)
        book_id = data["book_id"]
        book = Book.objects.get(pk = book_id)

        new_review = Review.objects.create(
            user = request.user,
            book = book,
            is_recommended = bool(data["is_recommended"]),
            rating = int(data["rating"]),
            book_review_desc = data["book_review_desc"]
        )
        new_review.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)

# NEW FOR MOBDEV
def get_book_by_id_json_mob(request, id):
    book = Book.objects.get(pk=id)
    book_data = {
        'model': "book.book",
        'pk': id,
        'fields':{
            'ISBN': book.ISBN,
            'title': book.title,
            'author': book.author,
            'year': book.year,
            'publisher': book.publisher,
            'image_s': book.image_s,
            'image_m': book.image_m,
            'image_l': book.image_l
        }
    }
    print(book_data)
    return JsonResponse(book_data)

def get_rev_by_user_json_mob(request):
    user = request.user
    reviews = Review.objects.filter(user=user)
    review_data = []
    for review in reviews:
        review_data.append({
            'model': 'reviews.review',
            'pk' : review.pk,
            'fields':{
                'user': review.user.pk,
                'book': review.book.pk,
                'book_review_desc': review.book_review_desc,
                'rating': review.rating,
                'is_recommended': review.is_recommended,
                'date_added': review.date_added,
            }
        })
    return HttpResponse(serializers.serialize('json', reviews))

# def get_rev_by_user_json_mob(request):
#     user = request.user
#     reviews = Review.objects.filter(user=user)
#     review_data = []
#     for review in reviews:
#         review_data.append({
#             'model': 'reviews.review',
#             'pk' : review.pk,
#             'fields':{
#                 'user': review.user.pk,
#                 'book': review.book.pk,
#                 'book_review_desc': review.book_review_desc,
#                 'rating': review.rating,
#                 'is_recommended': review.is_recommended,
#                 'date_added': review.date_added,
#             }
#         })
    # return HttpResponse(serializers.serialize('json', reviews))

    # return JsonResponse({'reviews': review_data})
def get_rev_by_book_json_mob(request, id):
    book = Book.objects.get(pk=id)
    reviews = Review.objects.filter(book = book)
    review_data = []
    for review in reviews:
        review_data.append({
            'model': 'reviews.review',
            'pk' : review.pk,
            'fields':{
                'user': review.user.pk,
                'book': review.book.pk,
                'book_review_desc': review.book_review_desc,
                'rating': review.rating,
                'is_recommended': review.is_recommended,
                'date_added': review.date_added,
            }
        })
    return HttpResponse(serializers.serialize('json', reviews))

def get_user_by_id_mob(request, id):
    user = User.objects.get(pk=id)
    user_data = user.username
    return HttpResponse(user_data)

