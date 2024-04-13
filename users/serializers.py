from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id','username', 'email','is_active',
                  'first_name', 'last_name', 'is_superuser', 'last_login',
                   'permissions', 'profile_picture', 'birthdate', 'description', 'phone']

    def get_permissions(self, obj):
        return obj.get_all_permissions()