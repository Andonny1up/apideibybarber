from django.urls import path
from .views import UserProfileView , UserList, UserDetail

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('users/', UserList.as_view(), name='user_list'),
    path('users/<int:pk>/', UserDetail.as_view(), name='user_detail'),
]