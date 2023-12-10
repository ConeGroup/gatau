from django.urls import path, include
from userprofile.views import show_userprofile
from home.views import home, user_home
from userprofile.views import edit_profile
from userprofile.views import change_password
from userprofile.views import edit_profile_ajax
from userprofile.views import change_password_ajax, show_userprofile_api

app_name = 'userprofile'

urlpatterns = [
    path('', show_userprofile, name='show_userprofile'),
    path('user-page/', user_home, name='user_home'),
    path('edit_profile',edit_profile, name = 'edit_profile'),
    path('edit_profile_ajax',edit_profile_ajax, name = 'edit_profile_ajax'),
    path('change-password', change_password, name='change-password'),
    path('change_password_ajax', change_password_ajax, name='change_password_ajax'),
    path('api/show_userprofile/', show_userprofile_api, name='show_userprofile_api'),
]