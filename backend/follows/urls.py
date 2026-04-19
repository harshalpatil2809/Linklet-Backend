from django.urls import path
from .views import FollowToggleView

urlpatterns = [
    path('toggle/<int:user_id>/', FollowToggleView.as_view(), name='follow-toggle'),
]