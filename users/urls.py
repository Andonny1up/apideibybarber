from django.urls import path
from .views import UserProfileView , UserList, UserDetail, GroupListView

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('users/', UserList.as_view(), name='user_list'),
    path('users/<int:pk>/', UserDetail.as_view(), name='user_detail'),
    path('groups/', GroupListView.as_view(), name='group-list'),
]