from django.urls import path
from reviews.views import show_main, get_book_json, add_review_ajax, create_review, add_review_form, review_page, back_to_main, get_review_by_user_json, get_book_by_id_json
from reviews.views import get_review_json, book_details, update_review, get_review_by_id_json

app_name = 'reviews'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('get-book-json/', get_book_json, name='get_book_json'),
    path('get-review-json/', get_review_json, name='get_review_json'),
    path('get-book-by-id/<int:id>/', get_book_by_id_json, name='get_book_by_id_json'),
    path('get-review-by-id/<int:id>/', get_review_by_id_json, name='get_review_by_id_json'),
    path('get-review-by-user/', get_review_by_user_json, name='get_review_by_user_json'),
    path('add-review/', add_review_ajax, name='add_review_ajax'),
    path('review-page/', review_page, name='review_page'),
    path('back_main/', back_to_main, name='back_to_main'),
    path('book-details/<int:book_id>/', book_details, name='book_details'),
    path('update_review/<int:review_id>/', update_review, name='update_review'),

    path('create-review', create_review, name='create_review'),
    path('add-review-form/', add_review_form, name='add_review_form'),

]