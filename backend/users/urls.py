from django.urls import path
from .views import register, login,logout,google_login_callback,get_user

urlpatterns = [
    path('register/', register,name='user_register'),
    path('login/', login),
    path('logout/', logout),
    path('google/callback/', google_login_callback, name='google_callback'),
    path('user/', get_user )
]