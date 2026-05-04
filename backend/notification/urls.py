from django.urls import path
from . import views

urlpatterns = [
    path('history/', views.get_notifications, name='get-notifications'),
]