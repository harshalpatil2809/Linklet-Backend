from django.urls import path
from .views import SendMessageView,MessageHistoryView,InboxListView

urlpatterns = [
    path('send/<int:user_id>/', SendMessageView.as_view(), name='send-message'),
    path('history/<int:user_id>/', MessageHistoryView.as_view(), name='message-history'),
    path('inbox/', InboxListView.as_view(), name='inbox-list'),
]