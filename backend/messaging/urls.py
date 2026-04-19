from django.urls import path
from .views import SendMessageView,MessageHistoryView,InboxListView

urlpatterns = [
    path('send/<str:username>/', SendMessageView.as_view(), name='send-message'),
    path('history/<str:username>/', MessageHistoryView.as_view(), name='message-history'),
    path('inbox/', InboxListView.as_view(), name='inbox-list'),
]