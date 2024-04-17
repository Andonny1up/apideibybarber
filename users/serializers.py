from rest_framework import serializers, exceptions
from .models import CustomUser
from django.contrib.auth.models import Group, Permission

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']
        

class UserSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()
    groups = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id','username','password', 'email','is_active',
                  'first_name', 'last_name', 'is_superuser', 'last_login',
                   'permissions','groups', 'profile_picture', 'birthdate', 'description', 'phone']
        extra_kwargs = {'password': {'write_only': True, 'required': False}}


    def get_permissions(self, obj):
        return obj.get_all_permissions()
    

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        if password is None:
            raise exceptions.ValidationError({"password": "Este campo es obligatorio."})
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user
    

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        group = validated_data.pop('groups', None)
        user = super().update(instance, validated_data)
        
        if group is None:
            user.groups.clear()
        elif group is not None:
            user.groups.clear()
            user.groups.set(group)

        if password is not None:
            user.set_password(password)
        user.save()
        return user