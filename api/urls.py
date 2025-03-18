from django.urls import path, include
from api.view.ContactView import ContactUsView
from api.view.OrderView import OrderCreateView, OrderListView, OrderDetailView
from api.view.CustomerView import (
    CustomerRetrieveView, 
    CustomerUpdateView, 
    CustomerRegisterView, 
    CustomAuthToken, 
    CustomerListView, 
    RefreshTokenView,
    LogoutView
)
from api.view.ProductView import (
    ProductListView,
    ProductCreateView,
    ProductRetrieveView,
    ProductUpdateView,
    ProductDeleteView,
    ProductByCategoryView
)
from api.view.CategoryView import (
    CategoryListView,
    CategoryCreateView,
    CategoryRetrieveView,
    CategoryUpdateView,
    CategoryDeleteView
)
from rest_framework import routers
from api.view.SubcategoryView import (
    SubcategoryListView,
    SubcategoryCreateView,
    SubcategoryRetrieveView,
    SubcategoryUpdateView,
    SubcategoryDeleteView
)
from api.view.OrderItemView import (
    OrderItemListView, OrderItemRetrieveView, OrderItemCreateView,
    OrderItemUpdateView, OrderItemDeleteView
)
from api.view.CouponView import (
    CouponListView, CouponRetrieveView, CouponValidateView,
    CouponCreateView, CouponUpdateView, CouponDeleteView
)
from api.view.DiscountView import (
    DiscountListView,
    DiscountRetrieveView,
    DiscountCreateView,
    DiscountUpdateView,
    DiscountDeleteView
)

router = routers.DefaultRouter()

urlpatterns = [
    # Customers
    path('customers/', CustomerListView.as_view(), name='customer-list'),
    path("customer/profile/", CustomerRetrieveView.as_view(), name="customer-profile"),
    path("customer/update/", CustomerUpdateView.as_view(), name="customer-update"),
    # path("customer/register/", CustomerRegisterView.as_view(), name="customer-register"),
    
    path("login/", CustomAuthToken.as_view(), name="customer-login"),
    path('register/', CustomerRegisterView.as_view(), name='register'),  # Registro de usuario
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh-cookie/', RefreshTokenView.as_view(), name='refresh_cookie'),  # Renovación personalizada con cookies
    
    # Productos
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/create/', ProductCreateView.as_view(), name='product-create'),
    path('products/<str:name>/', ProductRetrieveView.as_view(), name='product-retrieve'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    path('products/category/<str:category_name>/', ProductByCategoryView.as_view(), name='product-by-category'),

    
    # Categorías
    path('categories/', CategoryListView.as_view(), name='category-list'),  # GET para listar
    path('categories/create/', CategoryCreateView.as_view(), name='category-create'),  # POST para crear
    path('categories/<str:name>/', CategoryRetrieveView.as_view(), name='category-detail'),  # GET para detalle
    path('categories/<int:pk>/update/', CategoryUpdateView.as_view(), name='category-update'),  # PUT para actualizar
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category-delete'),  
    
    # Subcategorías (usando las vistas separadas)
    path('subcategories/', SubcategoryListView.as_view(), name='subcategory-list'),
    path('subcategories/create/', SubcategoryCreateView.as_view(), name='subcategory-create'),
    path('subcategories/<str:name>/', SubcategoryRetrieveView.as_view(), name='subcategory-detail'),
    path('subcategories/<int:pk>/update/', SubcategoryUpdateView.as_view(), name='subcategory-update'),
    path('subcategories/<int:pk>/delete/', SubcategoryDeleteView.as_view(), name='subcategory-delete'),
     
    # Órdenes
    path('orders/', OrderListView.as_view(), name='order-list'),  # Lista solo las órdenes del usuario autenticado
    path('orders/create/', OrderCreateView.as_view(), name='order-create'),  # Crear una nueva orden
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),  # Ver detalles de una orden específica
    
    #Items de Ordenes 
    path("orders/<int:order_id>/items/", OrderItemListView.as_view(), name="orderitem-list"),  # Listar productos de una orden
    path("orders/items/<int:item_id>/", OrderItemRetrieveView.as_view(), name="orderitem-detail"),  # Obtener detalles de un producto en la orden
    path("orders/items/create/", OrderItemCreateView.as_view(), name="orderitem-create"),  # Agregar un producto a la orden
    path("orders/items/<int:item_id>/update/", OrderItemUpdateView.as_view(), name="orderitem-update"),  # Modificar cantidad de producto
    path("orders/items/<int:item_id>/delete/", OrderItemDeleteView.as_view(), name="orderitem-delete"),  # Eliminar un producto de la orden
    
    #Cupones
    path("coupons/", CouponListView.as_view(), name="coupon-list"),  # Listar cupones (admin)
    path("coupons/<str:code>/", CouponRetrieveView.as_view(), name="coupon-detail"),  # Obtener cupón (admin)
    path("coupons/create/", CouponCreateView.as_view(), name="coupon-create"),  # Crear cupón (admin)
    path("coupons/<str:code>/update/", CouponUpdateView.as_view(), name="coupon-update"),  # Actualizar cupón (admin)
    path("coupons/<str:code>/delete/", CouponDeleteView.as_view(), name="coupon-delete"),  # Eliminar cupón (admin)
    path("coupons/validate/", CouponValidateView.as_view(), name="coupon-validate"),  # Validar cupón
    
    #Descuentos
    path('discounts/', DiscountListView.as_view(), name='discount-list'),
    path('discounts/<int:pk>/', DiscountRetrieveView.as_view(), name='discount-detail'),
    path('discounts/create/', DiscountCreateView.as_view(), name='discount-create'),
    path('discounts/<int:pk>/update/', DiscountUpdateView.as_view(), name='discount-update'),
    path('discounts/<int:pk>/delete/', DiscountDeleteView.as_view(), name='discount-delete'),
    
    #Contacto
    path("contact/", ContactUsView.as_view(), name="contact-us"),

    # Enrutador para otras rutas ViewSet (si es necesario)
    path('', include(router.urls)),
]
