from django.urls import path
from bookrequest.views import show_request_page, create_request, remove_request, update_request
from bookrequest.views import get_request_item_json
from home.views import logout_user

app_name = 'bookrequest'

urlpatterns = [
    path('', show_request_page, name='show_request_page'),
    path('../logout/', logout_user, name='logout'),
    path('get-request-item/', get_request_item_json, name='get_request_item_json'),
    path('create-request/', create_request, name='create_request'),
    path('remove-request/<int:id>', remove_request, name='remove_request'),
    path('update-request/<int:id>', update_request, name='update_request'),
    ]