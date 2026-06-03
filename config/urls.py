from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from inventario.views import TipoEquipoViewSet, EquipoViewSet

router = DefaultRouter()
router.register(r'tipos', TipoEquipoViewSet)
router.register(r'equipos', EquipoViewSet)

urlpatterns = [
    path('backend/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG and hasattr(settings, 'MEDIA_ROOT'):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    