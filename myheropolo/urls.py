from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # Solo se incluye api.urls

    # Swagger JSON Schema
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    # Swagger UI
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'),
         name='swagger-ui'),

    # Redoc UI (otra alternativa)
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

# if settings.DEBUG:
#     urlpatterns += staticfiles_urlpatterns()
