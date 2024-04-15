from rest_framework import serializers, exceptions
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id','username','password', 'email','is_active',
                  'first_name', 'last_name', 'is_superuser', 'last_login',
                   'permissions', 'profile_picture', 'birthdate', 'description', 'phone']
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
        user = super().update(instance, validated_data)
        if password is not None:
            user.set_password(password)
        user.save()
        return user