from django.urls import path
from collection.views import add_book_to_collection, add_book_to_collection_ajax, remove_book_from_collection, show_collection, create_collection_ajax, delete_collection, edit_collection, get_book_json, get_collection_json, show_json, show_json_by_id

app_name = 'collection'

urlpatterns = [
    path('', show_collection, name='show_collection'),
    path('add-book-to-collection-ajax/', add_book_to_collection_ajax, name='add_book_to_collection_ajax'),
    path('create-collection-ajax/', create_collection_ajax, name='create_collection_ajax'),
    path('edit-collection/<int:collection_id>/', edit_collection, name='edit_collection'),
    path('delete_collection/<int:collection_id>/', delete_collection, name='delete_collection'),
    path('get-collection-json/', get_collection_json, name='get_collection_json'),  # Tambahkan ini
    path('get-book-json/', get_book_json, name='get_book_json'),  # Tambahkan ini
    path('json/', show_json, name='show_json'),
    path('json/<int:id>/', show_json_by_id, name='show_json_by_id'), 
    path('<int:collection_id>/add-book/', add_book_to_collection, name='add_book_to_collection'),
    path('<int:collection_id>/remove-book/<int:book_id>/', remove_book_from_collection, name='remove_book_from_collection'),
]
