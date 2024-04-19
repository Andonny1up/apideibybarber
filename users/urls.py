from django.urls import path
from .views import UserProfileView , UserList, UserDetail
from .views import GroupListView, GroupDetailView, AllGroupListView
from .views import AllPermissionListView, PermissionListView, PermissionDetailView, ContentTypeListView

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('users/', UserList.as_view(), name='user_list'),
    path('users/<int:pk>/', UserDetail.as_view(), name='user_detail'),
    path('allgroups/', AllGroupListView.as_view(), name='allgroup_list'),
    path('groups/', GroupListView.as_view(), name='group_list'),
    path('groups/<int:pk>/', GroupDetailView.as_view(), name='group_detail'),
    path('all-permissions/', AllPermissionListView.as_view(), name='all_permission_list'),
    path('permissions/', PermissionListView.as_view(), name='permission_list'),
    path('permissions/<int:pk>/', PermissionDetailView.as_view(), name='permission_detail'),
    path('contenttypes/', ContentTypeListView.as_view(), name='contenttype_list'),
]