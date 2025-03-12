from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from api.model.ProductModel import Product
from api.serializers.ProductSerializer import ProductSerializer


class ProductPagination(PageNumberPagination):
    """
    Paginación para los productos, con un máximo de 100 productos por página.
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


@extend_schema(
    summary="Lista productos",
    description="Obtiene una lista de productos con paginación, filtros y opciones de búsqueda.",
    responses={200: ProductSerializer(many=True)},
    parameters=[
        OpenApiParameter(name="page", description="Número de página", required=False, type=int),
        OpenApiParameter(name="page_size", description="Cantidad de productos por página", required=False, type=int),
        OpenApiParameter(name="category", description="Filtrar por ID de categoría", required=False, type=int),
        OpenApiParameter(name="subcategory", description="Filtrar por ID de subcategoría", required=False, type=int),
        OpenApiParameter(name="search", description="Buscar en nombre o descripción", required=False, type=str),
        OpenApiParameter(name="ordering", description="Ordenar por precio o fecha de creación", required=False, type=str,
                         enum=["price", "-price", "created_at", "-created_at"])
    ]
)
class ProductListView(generics.ListAPIView):
    """
    API para listar productos.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['category', 'subcategory']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at']


@extend_schema(
    summary="Crea un nuevo producto",
    description="Crea un nuevo producto con los datos proporcionados.",
    request=ProductSerializer,
    responses={
        201: ProductSerializer,
        400: OpenApiResponse(description="Error de validación")
    }
)
class ProductCreateView(generics.CreateAPIView):
    """
    API para crear un nuevo producto.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


@extend_schema(
    summary="Obtiene un producto específico",
    description="Recupera los detalles de un producto específico por su ID.",
    responses={
        200: ProductSerializer,
        404: OpenApiResponse(description="No encontrado")
    }
)
class ProductRetrieveView(generics.RetrieveAPIView):
    """
    API para obtener un producto específico.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


@extend_schema(
    summary="Actualiza un producto específico",
    description="Actualiza un producto específico por su ID.",
    request=ProductSerializer,
    responses={
        200: ProductSerializer,
        400: OpenApiResponse(description="Error de validación"),
        404: OpenApiResponse(description="No encontrado")
    }
)
class ProductUpdateView(generics.UpdateAPIView):
    """
    API para actualizar un producto específico.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


@extend_schema(
    summary="Elimina un producto específico",
    description="Elimina un producto específico por su ID.",
    responses={
        204: OpenApiResponse(description="Eliminado exitosamente"),
        404: OpenApiResponse(description="No encontrado")
    }
)
class ProductDeleteView(generics.DestroyAPIView):
    """
    API para eliminar un producto específico.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
