from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import DjangoModelPermissions ,IsAuthenticated
from django.db.models import Q, Value as V
from django.db.models.functions import Concat
from .paginations import CustomPageNumberPagination
from .serializers import UserSerializer, GroupSerializer, PermissionSerializer, ContentTypeSerializer
from .models import CustomUser
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
# Create your views here.


class UserProfileView(APIView):

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    

class UserList(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        include_deleted = self.request.query_params.get('include_deleted', 'false')
        queryset = CustomUser.objects.all()
        if include_deleted.lower() != 'true':
            queryset = queryset.filter(deleted_at__isnull=True)

        search_param = self.request.query_params.get('search', None)
        if search_param is not None:
            full_name = Concat('first_name', V(' '), 'last_name')
            queryset = queryset.annotate(full_name=full_name).filter(
                Q(full_name__icontains=search_param) |
                Q(username__icontains=search_param)
            )

        return queryset

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.filter(deleted_at__isnull=True)
    serializer_class = UserSerializer
    permission_classes = [DjangoModelPermissions]


# Groups
class AllGroupListView(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [DjangoModelPermissions]
    
    
class GroupListView(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        queryset = Group.objects.all()

        search_param = self.request.query_params.get('search', None)
        if search_param is not None:
            queryset = queryset.filter(name__icontains=search_param)
        
        return queryset

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        permissions = Permission.objects.all()
        response.data['available_permissions'] = PermissionSerializer(permissions, many=True).data
        return response
    

class GroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [DjangoModelPermissions]


class AllPermissionListView(APIView):
    def get(self, request):
        permissions = Permission.objects.all()
        serializer = PermissionSerializer(permissions, many=True)
        return Response(serializer.data)

# Permissions
class PermissionListView(generics.ListCreateAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = [DjangoModelPermissions]
    
    def get_queryset(self):
        queryset = Permission.objects.all()

        search_param = self.request.query_params.get('search', None)
        if search_param is not None:
            queryset = queryset.filter(name__icontains=search_param)
        
        return queryset
    

class PermissionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [DjangoModelPermissions]
    

class ContentTypeListView(generics.ListAPIView):
    queryset = ContentType.objects.all()
    serializer_class = ContentTypeSerializer