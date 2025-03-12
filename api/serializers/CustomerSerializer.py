from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Customer
from django.contrib.auth.hashers import make_password

class CustomerRegisterSerializer(serializers.ModelSerializer):
    """Serializer solo para el registro (email y password)"""
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["email", "password"]

    def validate_password(self, value):
        """Valida que la contraseña tenga al menos 8 caracteres y un número"""
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("La contraseña debe contener al menos un número.")
        return value

    def create(self, validated_data):
        """Crea un usuario con email y password, y un Customer vacío"""
        email = validated_data["email"]
        password = validated_data["password"]

        user = User(username=email, email=email)
        user.set_password(password)  # 🔥 Hashea automáticamente la contraseña
        user.save()

        Customer.objects.create(user=user)  # Crea perfil de cliente vacío

        return user


class UserSerializer(serializers.ModelSerializer):
    """Serializador para los datos del usuario relacionado."""
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email']

class CustomerSerializer(serializers.ModelSerializer):
    """Incluye los datos del usuario relacionado."""
    user = UserSerializer(read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'phone', 'address', 'created_at', 'user']
        
class CustomerUpdateSerializer(serializers.ModelSerializer):
    # Campos relacionados con el modelo User
    first_name = serializers.CharField(source="user.first_name", required=False)
    last_name = serializers.CharField(source="user.last_name", required=False)
    email = serializers.EmailField(source="user.email", required=False)

    class Meta:
        model = Customer
        fields = ['phone', 'address', 'first_name', 'last_name', 'email']  # Todos los campos que deseas actualizar

    def update(self, instance, validated_data):
        # Procesar datos del Customer
        user_data = validated_data.pop('user', {})  # Extraer datos relacionados al usuario
        instance.phone = validated_data.get('phone', instance.phone)
        instance.address = validated_data.get('address', instance.address)
        instance.save()

        # Procesar datos del User
        user = instance.user
        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)
        user.email = user_data.get('email', user.email)
        user.save()

        return instance
