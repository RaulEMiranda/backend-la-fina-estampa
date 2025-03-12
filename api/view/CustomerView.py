from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from api.serializers.CustomerSerializer import CustomerSerializer, CustomerRegisterSerializer, CustomerUpdateSerializer
from api.model.CustomerModel import Customer
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAdminUser
from api.utils import send_welcome_email  


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
        customer = Customer.objects.get(user=request.user)
        serializer = CustomerUpdateSerializer(
            customer, data=request.data, partial=True)

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
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            send_welcome_email(user.email, user.username)
            return Response({"token": token.key}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary="Autenticar usuario y obtener token",
    description="Devuelve el token de autenticación de un usuario registrado.",
    responses={200: {"token": "string"}, 400: {
        "detail": "Credenciales inválidas"}}
)
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data["token"])
        return Response({"token": token.key})


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
