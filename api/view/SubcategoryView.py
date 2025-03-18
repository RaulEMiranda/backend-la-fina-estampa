from rest_framework import generics
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from api.model.SubcategoryModel import Subcategory
from api.serializers.SubcategorySerializer import SubcategorySerializer


@extend_schema(
    summary="Lista las subcategorías",
    description="Obtiene una lista de subcategorías con opción de filtrar por categoría usando el parámetro `category_name`.",
    parameters=[
        OpenApiParameter(
            name="category_name",
            type=str,
            location=OpenApiParameter.QUERY,
            required=False,
            description="Filtrar subcategorías por nombre de categoría"
        )
    ],
    responses={200: SubcategorySerializer(many=True)}
)
class SubcategoryListView(generics.ListAPIView):
    """
    API para listar subcategorías.  
    Se puede filtrar por `category_name` en la URL.
    """
    serializer_class = SubcategorySerializer

    def get_queryset(self):
        category_name = self.request.query_params.get('category_name')
        queryset = Subcategory.objects.all()
        
        if category_name:
            queryset = queryset.filter(category__name__iexact=category_name)  # Búsqueda insensible a mayúsculas/minúsculas
        
        return queryset


@extend_schema(
    summary="Crea una nueva subcategoría",
    description="Crea una nueva subcategoría con los datos proporcionados.",
    request=SubcategorySerializer,
    responses={
        201: SubcategorySerializer,
        400: OpenApiResponse(description="Error de validación")
    }
)
class SubcategoryCreateView(generics.CreateAPIView):
    """
    API para crear una nueva subcategoría.
    """
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer


@extend_schema(
    summary="Obtiene una subcategoría específica",
    description="Obtiene los detalles de una subcategoría específica por su ID.",
    responses={
        200: SubcategorySerializer,
        404: OpenApiResponse(description="No encontrado")
    }
)
class SubcategoryRetrieveView(generics.RetrieveAPIView):
    """
    API para obtener una subcategoría específica.
    """
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer
    lookup_field = "name"


@extend_schema(
    summary="Actualiza una subcategoría específica",
    description="Actualiza una subcategoría específica por su ID.",
    request=SubcategorySerializer,
    responses={
        200: SubcategorySerializer,
        400: OpenApiResponse(description="Error de validación"),
        404: OpenApiResponse(description="No encontrado")
    }
)
class SubcategoryUpdateView(generics.UpdateAPIView):
    """
    API para actualizar una subcategoría específica.
    """
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer


@extend_schema(
    summary="Elimina una subcategoría específica",
    description="Elimina una subcategoría específica por su ID.",
    responses={
        204: OpenApiResponse(description="Eliminado exitosamente"),
        404: OpenApiResponse(description="No encontrado")
    }
)
class SubcategoryDeleteView(generics.DestroyAPIView):
    """
    API para eliminar una subcategoría específica.
    """
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer
