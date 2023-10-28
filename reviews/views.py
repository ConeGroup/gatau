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



# Create your views here.
# @login_required(login_url='/login')
# @csrf_exempt
# def create_review(request):
#     if request.method == 'POST':
#         name = request.POST.get("name")
#         price = request.POST.get("price")
#         description = request.POST.get("description")
#         user = request.user

#         new_product = Product(name=name, price=price, description=description, user=user)
#         new_product.save()

#         return HttpResponse(b"CREATED", status=201)

#     return HttpResponseNotFound()

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
    context = {
        'user' : request.user,
        'books' : books,
        'reviews' : reviews,
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

# def get_user_reviews(request):
#     user = request.user
#     reviews = Review.objects.filter(user=user)
#     review_data = []

#     for review in reviews:
#         review_data.append({
#             'book_title': review.book.title,
#             'rating': review.rating,
#             'book_review_desc': review.book_review_desc,
#             'is_recommended': review.is_recommended,
#             'date_added': review.date_added,
#         })

#     return JsonResponse({'reviews': review_data})

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
    # data = Book.objects.filter(pk=id)
    # return HttpResponse(serializers.serialize("json", data), content_type="application/json")

# def get_review_by_user_json(request):
#     data = Review.objects.filter(user=request.user)
#     return HttpResponse(serializers.serialize("json", data), content_type="application/json")


def get_review_by_id_json(request, id):
    review = Review.get_object_or_404(pk=id)
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
        # Retrieve and validate updated data from request.POST or request data
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

        # Create a new Review object
        review = Review(
            user=request.user,
            book=book, 
            rating=rating,
            book_review_desc=book_review_desc,
            is_recommended=bool(is_recommended)
        )
        review.save()

        return HttpResponse(b"CREATED", status=201)

    # Handle other HTTP methods or render a form
    return HttpResponseNotFound()

def create_review(request):
    form = ReviewForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('reviews:show_main'))

    context = {'form': form}
    return render(request, "create_review.html", context)


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