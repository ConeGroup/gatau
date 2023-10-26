from django.urls import path
from loans.views import add_book_ajax, delete_book

app_name = 'loans'

urlpatterns = [
    path('create-book-ajax/', add_book_ajax, name='add_book_ajax'),
    path('delete_book/<int:book_id>', delete_book, name='delete_book'),
]