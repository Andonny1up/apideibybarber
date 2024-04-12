from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import DjangoModelPermissions ,IsAuthenticated
from django.db.models import Q
from .paginations import CustomPageNumberPagination
from .serializers import UserSerializer
from .models import CustomUser
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
        queryset = CustomUser.objects.all()
        search_param = self.request.query_params.get('search', None)
        if search_param is not None:
            queryset = queryset.filter(Q(first_name__icontains=search_param) |
                                       Q(last_name__icontains=search_param))

        return queryset

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [DjangoModelPermissions]