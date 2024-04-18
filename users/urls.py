from django.urls import path
from .views import UserProfileView , UserList, UserDetail
from .views import GroupListView, GroupDetailView, PermissionListView, AllPermissionListView

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('users/', UserList.as_view(), name='user_list'),
    path('users/<int:pk>/', UserDetail.as_view(), name='user_detail'),
    path('groups/', GroupListView.as_view(), name='group_list'),
    path('groups/<int:pk>/', GroupDetailView.as_view(), name='group_detail'),
    path('all-permissions/', AllPermissionListView.as_view(), name='all_permission_list'),
    path('permissions/', PermissionListView.as_view(), name='permission_list'),
]