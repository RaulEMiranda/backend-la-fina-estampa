from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from api.model.ProductModel import Product
from api.serializers.ProductSerializer import ProductSerializer
from django.shortcuts import get_object_or_404
from api.model.CategoryModel import Category
from api.model.SubcategoryModel import Subcategory

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
        OpenApiParameter(name="search", description="Buscar en nombre o descripción", required=False, type=str),
        OpenApiParameter(name="ordering", description="Ordenar por precio o nombre", required=False, type=str,
                         enum=["price", "-price", "name", "-name"])
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

    search_fields = ['name', 'description']
    ordering_fields = ['price', 'name']


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


@extend_schema(
    summary="Lista productos por nombre de categoría",
    description="Obtiene una lista de productos que pertenecen a una categoría específica según su nombre, con paginación y filtros.",
    responses={200: ProductSerializer(many=True)},
    parameters=[
        OpenApiParameter(name="subcategory", description="Filtrar por nombre de subcategoría", required=False, type=str)
    ]
)
class ProductByCategoryView(generics.ListAPIView):
    """
    API para listar productos de una categoría específica por nombre, con paginación y filtros.
    """
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['price', 'name']

    def get_queryset(self):
        category_name = self.kwargs.get('category_name')
        category = get_object_or_404(Category, name=category_name)
        queryset = Product.objects.filter(category=category).order_by("name")
        
        subcategory_name = self.request.query_params.get('subcategory')
        if subcategory_name:
            queryset = queryset.filter(subcategory__name=subcategory_name)
        
        return queryset