from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import DjangoModelPermissions ,IsAuthenticated
from .paginations import CustomPageNumberPagination
from .serializers import UserSerializer
from .models import CustomUser
# Create your views here.


class UserProfileView(APIView):

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    

class UserList(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = [DjangoModelPermissions]

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [DjangoModelPermissions]