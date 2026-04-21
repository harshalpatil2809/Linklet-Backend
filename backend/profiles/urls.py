from django.urls import path
from .views import ProfileDetailView,ProfileSearchView,MutualFollowListView,FollowersListView,FollowingListView,TargetUserProfileView

urlpatterns = [
    path('me/', ProfileDetailView.as_view(), name='profile-detail'),
    path('search/', ProfileSearchView.as_view(), name='profile-search'),
    path('mutual/', MutualFollowListView.as_view(), name='mutual-friends'),
    path('followers/', FollowersListView.as_view(), name='followers-list'),
    path('following/', FollowingListView.as_view(), name='followers-list'),
    path('target/<str:username>/', TargetUserProfileView.as_view(),name='target-profile')
]