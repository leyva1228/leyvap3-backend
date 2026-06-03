import os
from django.conf import settings
from django.db.models.deletion import ProtectedError
from django.http import FileResponse, Http404, JsonResponse
from rest_framework import filters, status, viewsets
from .models import TipoEquipo, Equipo
from .serializers import TipoEquipoSerializer, EquipoSerializer


class TipoEquipoViewSet(viewsets.ModelViewSet):
    queryset = TipoEquipo.objects.all()
    serializer_class = TipoEquipoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'descripcion', 'departamento']
    ordering_fields = ['nombre', 'fecha_creacion', 'departamento']

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            return JsonResponse(
                {'error': 'No se puede eliminar: este tipo tiene equipos asociados.'},
                status=status.HTTP_409_CONFLICT,
            )


class EquipoViewSet(viewsets.ModelViewSet):
    queryset = Equipo.objects.select_related('tipo_equipo').all()
    serializer_class = EquipoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'codigo', 'estado', 'tipo_equipo__nombre']
    ordering_fields = ['nombre', 'codigo', 'estado', 'fecha_adquisicion']


def media_serve(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if not os.path.exists(file_path):
        raise Http404(f"File not found: {file_path}")
    return FileResponse(open(file_path, 'rb'))
    