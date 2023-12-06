from django.urls import path
from reviews.views import show_main, get_book_json, add_review_ajax, review_sheet, review_page, back_to_main, get_review_by_user_json, get_book_by_id_json
from reviews.views import get_review_json, book_details, edit_review, get_review_by_id_json, delete_review, get_book_user, get_book_by_id_json_mob

app_name = 'reviews'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('get-book-json/', get_book_json, name='get_book_json'),
    path('get-book-user/', get_book_user, name='get_book_user'),
    path('get-review-json/', get_review_json, name='get_review_json'),
    path('get-book-by-id/<int:id>/', get_book_by_id_json, name='get_book_by_id_json'),
    path('get-review-by-id/<int:id>/', get_review_by_id_json, name='get_review_by_id_json'),
    path('get-review-by-user/', get_review_by_user_json, name='get_review_by_user_json'),
    path('add-review/', add_review_ajax, name='add_review_ajax'),
    path('review-page/', review_page, name='review_page'),
    path('review-sheet/<int:id>', review_sheet, name='review_sheet'),
    path('back_main/', back_to_main, name='back_to_main'),
    path('book-details/<int:book_id>/', book_details, name='book_details'),
    path('edit-review/<int:review_id>/', edit_review, name='edit_review'),
    path('delete-review/<int:id>/', delete_review, name='delete_review'),
    path('get-book-by-id-mob/<int:id>/', get_book_by_id_json_mob, name='get_book_by_id_json_mob'),

]