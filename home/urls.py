from django.urls import path
from home.views import home, user_home
from home.views import logout_user, login_user
from home.views import register

urlpatterns = [
    path('', home, name='home'),
    path('user-page/', user_home, name='user_home'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register, name='register'),
]