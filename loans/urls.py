from django.urls import path
from loans.views import show_loans, add_book_ajax, delete_book, get_product_json, get_book_json

app_name = 'loans'

urlpatterns = [
    path('', show_loans, name='show_loans'),
    path('create-book-ajax/', add_book_ajax, name='add_book_ajax'),
    path('delete_book/<int:book_id>', delete_book, name='delete_book'),
    path('get_product_json/', get_product_json, name='get_product_json'),
    path('get_book_json/', get_book_json, name='get_book_json'),
]