from rest_framework import serializers, exceptions
from .models import CustomUser
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

class ContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentType
        fields = ['id', 'app_label', 'model', 'name']


class PermissionSerializer(serializers.ModelSerializer):
    content_type = serializers.PrimaryKeyRelatedField(
        queryset=ContentType.objects.all()
    )
    content_type_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Permission
        fields = ['id', 'name', 'content_type','content_type_name', 'codename']

    def get_content_type_name(self, obj):
        return obj.content_type.name


class GroupSerializer(serializers.ModelSerializer):
    permissions = serializers.PrimaryKeyRelatedField(many=True, queryset=Permission.objects.all())

    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions']

    def create(self, validated_data):
        permissions = validated_data.pop('permissions', None)
        group = super().create(validated_data)
        if permissions is not None:
            group.permissions.set(permissions)
        return group
        

class UserSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()
    groups = serializers.PrimaryKeyRelatedField(many=True, queryset=Group.objects.all())
    groups_detail = GroupSerializer(source='groups', many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id','username','password', 'email','is_active',
                  'first_name', 'last_name', 'is_superuser', 'last_login',
                   'permissions','groups','groups_detail', 'profile_picture', 'birthdate', 'description', 'phone']
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
        print('VALIDATED DATA',validated_data)
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