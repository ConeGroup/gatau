from django.urls import path
from collection.views import add_book_to_collection_ajax, collection_list, create_collection_ajax, delete_collection, edit_collection, get_book_json, get_collections_json

app_name = 'collection'

urlpatterns = [
    path('', collection_list, name='collection_list'),
    path('add_book_to_collection_ajax/', add_book_to_collection_ajax, name='add_book_to_collection_ajax'),
    path('create_collection_ajax/', create_collection_ajax, name='create_collection_ajax'),
    path('edit_collection/<int:collection_id>/', edit_collection, name='edit_collection'),
    path('delete_collection/<int:collection_id>/', delete_collection, name='delete_collection'),
    path('get_collections_json/', get_collections_json, name='get_collections_json'),  # Tambahkan ini
    path('get_book_json/', get_book_json, name='get_book_json'),  # Tambahkan ini
]
