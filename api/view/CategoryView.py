from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse
from api.models import Category
from api.serializers.CategorySerializer import CategorySerializer


@extend_schema(
    summary="Lista todas las categorías",
    description="Obtiene una lista de todas las categorías disponibles.",
    responses={200: CategorySerializer(many=True)}
)
class CategoryListView(generics.ListAPIView):
    """
    API para listar todas las categorías.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


@extend_schema(
    summary="Crea una nueva categoría",
    description="Crea una nueva categoría con los datos proporcionados.",
    request=CategorySerializer,
    responses={
        201: CategorySerializer,
        400: OpenApiResponse(description="Error de validación")
    }
)
class CategoryCreateView(generics.CreateAPIView):
    """
    API para crear una nueva categoría.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


@extend_schema(
    summary="Obtiene los detalles de una categoría específica",
    description="Recupera los detalles de una categoría específica por su ID.",
    responses={
        200: CategorySerializer,
        404: OpenApiResponse(description="No encontrado")
    }
)
class CategoryRetrieveView(generics.RetrieveAPIView):
    """
    API para obtener una categoría específica.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "name"


@extend_schema(
    summary="Actualiza una categoría específica",
    description="Actualiza una categoría específica por su ID.",
    request=CategorySerializer,
    responses={
        200: CategorySerializer,
        400: OpenApiResponse(description="Error de validación"),
        404: OpenApiResponse(description="No encontrado")
    }
)
class CategoryUpdateView(generics.UpdateAPIView):
    """
    API para actualizar una categoría específica.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


@extend_schema(
    summary="Elimina una categoría específica",
    description="Elimina una categoría específica por su ID.",
    responses={
        204: OpenApiResponse(description="Eliminado exitosamente"),
        404: OpenApiResponse(description="No encontrado")
    }
)
class CategoryDeleteView(generics.DestroyAPIView):
    """
    API para eliminar una categoría específica.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
