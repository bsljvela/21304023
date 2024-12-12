from rest_framework import serializers
from users.models import User
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name',
                  'last_name', 'password', 'is_active', 'is_staff']

class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Asegúrate de incluir estos campos
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            # La contraseña no se devolverá en la respuesta
            'password': {'write_only': True},
        }

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError(
                "La contraseña debe tener al menos 8 caracteres.")
        return value

    def create(self, validated_data):
        # Hashea la contraseña antes de guardar
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
