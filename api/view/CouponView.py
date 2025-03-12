from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django.utils.timezone import now
from api.serializers.CouponSerializer import CouponSerializer
from api.model.CouponModel import Coupon

# 📌 1. Listar todos los cupones (SOLO ADMIN)
@extend_schema(
    summary="Listar todos los cupones",
    description="Obtiene una lista de todos los cupones disponibles. Solo accesible para administradores.",
    responses={200: CouponSerializer(many=True), 403: {"detail": "No autorizado"}}
)
class CouponListView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        coupons = Coupon.objects.all()
        serializer = CouponSerializer(coupons, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# 📌 2. Obtener detalles de un cupón (SOLO ADMIN)
@extend_schema(
    summary="Obtener detalles de un cupón",
    description="Devuelve la información de un cupón específico, solo accesible para administradores.",
    parameters=[OpenApiParameter(name="code", description="Código del cupón", required=True, type=str)],
    responses={200: CouponSerializer, 404: {"detail": "Cupón no encontrado"}, 403: {"detail": "No autorizado"}}
)
class CouponRetrieveView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, code):
        try:
            coupon = Coupon.objects.get(code=code)
            serializer = CouponSerializer(coupon)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Coupon.DoesNotExist:
            return Response({"detail": "Cupón no encontrado"}, status=status.HTTP_404_NOT_FOUND)

# 📌 3. Validar un cupón para aplicarlo en una compra
@extend_schema(
    summary="Validar un cupón",
    description="Verifica si un cupón es válido para usar en una compra.",
    parameters=[OpenApiParameter(name="code", description="Código del cupón", required=True, type=str)],
    responses={200: CouponSerializer, 400: {"detail": "Cupón no válido o expirado"}}
)
class CouponValidateView(APIView):
    def get(self, request):
        code = request.query_params.get('code')
        try:
            coupon = Coupon.objects.get(code=code, is_active=True)
            if coupon.start_date <= now() <= coupon.end_date:
                serializer = CouponSerializer(coupon)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"detail": "Cupón expirado"}, status=status.HTTP_400_BAD_REQUEST)
        except Coupon.DoesNotExist:
            return Response({"detail": "Cupón no válido"}, status=status.HTTP_400_BAD_REQUEST)

# 📌 4. Crear un cupón (SOLO ADMIN)
@extend_schema(
    summary="Crear un cupón",
    description="Permite a los administradores crear un nuevo cupón.",
    request=CouponSerializer,
    responses={201: CouponSerializer, 400: {"detail": "Datos inválidos"}, 403: {"detail": "No autorizado"}}
)
class CouponCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        serializer = CouponSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 📌 5. Actualizar un cupón (SOLO ADMIN)
@extend_schema(
    summary="Actualizar un cupón",
    description="Permite a los administradores modificar un cupón existente.",
    request=CouponSerializer,
    responses={200: CouponSerializer, 400: {"detail": "Datos inválidos"}, 404: {"detail": "Cupón no encontrado"}, 403: {"detail": "No autorizado"}}
)
class CouponUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def put(self, request, code):
        try:
            coupon = Coupon.objects.get(code=code)
            serializer = CouponSerializer(coupon, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Coupon.DoesNotExist:
            return Response({"detail": "Cupón no encontrado"}, status=status.HTTP_404_NOT_FOUND)

# 📌 6. Eliminar un cupón (SOLO ADMIN)
@extend_schema(
    summary="Eliminar un cupón",
    description="Permite a los administradores eliminar un cupón.",
    responses={204: None, 404: {"detail": "Cupón no encontrado"}, 403: {"detail": "No autorizado"}}
)
class CouponDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def delete(self, request, code):
        try:
            coupon = Coupon.objects.get(code=code)
            coupon.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Coupon.DoesNotExist:
            return Response({"detail": "Cupón no encontrado"}, status=status.HTTP_404_NOT_FOUND)
