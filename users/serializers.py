from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'permissions', 'profile_picture', 'bithdate', 'description', 'phone']

    def get_permissions(self, obj):
        return obj.get_all_permissions()