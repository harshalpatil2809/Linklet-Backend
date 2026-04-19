from django.urls import path
from .views import FollowToggleView

urlpatterns = [
    path('toggle/<str:username>/', FollowToggleView.as_view(), name='follow-toggle'),
]