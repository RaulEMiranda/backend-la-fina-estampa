from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.exceptions import InvalidToken
from drf_spectacular.utils import extend_schema
from api.serializers.CustomerSerializer import CustomerSerializer, CustomerRegisterSerializer, CustomerUpdateSerializer
from api.model.CustomerModel import Customer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from api.utils import send_welcome_email  
from django.contrib.auth import authenticate


@extend_schema(
    summary="Obtener perfil del usuario",
    description="Devuelve la información del cliente autenticado, incluyendo nombre, dirección y teléfono.",
    responses={200: CustomerSerializer, 401: {"detail": "No autenticado"}}
)
class CustomerRetrieveView(APIView):
    """
    API para obtener el perfil del usuario autenticado.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        customer = Customer.objects.get(user=request.user)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    summary="Actualizar perfil del usuario",
    description="Permite a un usuario autenticado actualizar su nombre, apellido, email, teléfono y dirección.",
    request=CustomerUpdateSerializer,
    responses={200: CustomerUpdateSerializer, 400: {"detail": "Datos inválidos"}, 401: {"detail": "No autenticado"}}
)
class CustomerUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        try:
            customer = Customer.objects.get(user=request.user)
        except Customer.DoesNotExist:
            return Response({"detail": "No se encontró un cliente asociado a este usuario"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CustomerUpdateSerializer(customer, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(
    summary="Registrar nuevo usuario",
    description="Crea un nuevo usuario con email y password. No se requiere nombre, teléfono ni dirección en el registro.",
    request=CustomerRegisterSerializer,
    responses={201: {"token": "string"}, 400: {"detail": "Datos inválidos"}}
)
class CustomerRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CustomerRegisterSerializer(data=request.data)

        if serializer.is_valid():
            # Crear usuario
            user = serializer.save()

            # Crear tokens (Access y Refresh)
            refresh = RefreshToken.for_user(user)

            # Enviar correo de bienvenida
            send_welcome_email(user.email, user.username)

            # Configurar cookies HTTP-only para los tokens
            response = Response({"message": "Usuario registrado exitosamente"}, status=status.HTTP_201_CREATED)
            response.set_cookie(
                key='access',
                value=str(refresh.access_token),
                httponly=True,  # Solo accesible desde el servidor
                secure=True,    # Solo envía la cookie por HTTPS (asegúrate de usar HTTPS en producción)
                samesite='Strict',  # Protege contra CSRF
            )
            response.set_cookie(
                key='refresh',
                value=str(refresh),
                httponly=True,
                secure=True,
                samesite='Strict',
            )
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary="Autenticar usuario y obtener token",
    description="Autentica al usuario y configura tokens JWT en cookies HTTP-only.",
    responses={200: {"message": "Login exitoso"}, 401: {"detail": "Credenciales inválidas"}},
)
class CustomAuthToken(APIView):
    permission_classes = [AllowAny]  # Permitir el acceso público para login

    def post(self, request, *args, **kwargs):
        # Obtener credenciales del usuario
        email = request.data.get('email')
        password = request.data.get('password')

        # Autenticar usuario
        user = authenticate(username=email, password=password)
        if user is not None:
            # Generar tokens JWT
            refresh = RefreshToken.for_user(user)

            # Configurar cookies HTTP-only con los tokens
            response = Response({"message": "Login exitoso"}, status=status.HTTP_200_OK)
            response.set_cookie(
                key='access',
                value=str(refresh.access_token),
                httponly=True,
                secure=True,  # Asegúrate de usar HTTPS en producción
                samesite='Strict',
            )
            response.set_cookie(
                key='refresh',
                value=str(refresh),
                httponly=True,
                secure=True,
                samesite='Strict',
            )
            return response

        return Response({"detail": "Credenciales inválidas"}, status=status.HTTP_401_UNAUTHORIZED)

@extend_schema(
    summary="Listar todos los clientes",
    description="Devuelve una lista con todos los clientes registrados.",
    responses={200: CustomerSerializer(many=True)}
)
class CustomerListView(APIView):
    """
    API para listar todos los clientes.
    """
    permission_classes = [IsAdminUser]

    def get(self, request):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RefreshTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            # Obtener el Refresh Token de las cookies
            refresh_token = request.COOKIES.get('refresh')
            if not refresh_token:
                return Response({"error": "Refresh token no encontrado"}, status=status.HTTP_401_UNAUTHORIZED)

            # Crear nuevo Access Token
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)

            # Guardar el nuevo Access Token en la cookie
            response = Response({"message": "Token renovado correctamente"})
            response.set_cookie(
                key='access',
                value=access_token,
                httponly=True,
                secure=True,
                samesite='Strict',
            )
            return response
        except InvalidToken:
            return Response({"error": "Refresh token inválido"}, status=status.HTTP_401_UNAUTHORIZED)   
        
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = Response({"message": "Logout exitoso"}, status=status.HTTP_200_OK)
        response.delete_cookie('access')
        response.delete_cookie('refresh')
        return response