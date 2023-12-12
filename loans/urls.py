from django.urls import path
from loans.views import show_loans, add_book_ajax, delete_book, get_product_json, get_book_json, show_loans_page, create_loans_flutter
from home.views import home, user_home

app_name = 'loans'

urlpatterns = [
    path('', show_loans, name='show_loans'),
    path('create-book-ajax/', add_book_ajax, name='add_book_ajax'),
    path('delete_book/<int:book_id>', delete_book, name='delete_book'),
    path('get_product_json/', get_product_json, name='get_product_json'),
    path('get_book_json/', get_book_json, name='get_book_json'),
    path('show_loans_page/', show_loans_page, name='show_loans_page'),
    path('', home, name='home'),
    path('user-page/', user_home, name='user_home'),
    path('create-loans-flutter/', create_loans_flutter, name='create_loans_flutter'),
]