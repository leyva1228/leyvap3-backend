from django.contrib import admin
from .models import TipoEquipo, Equipo


@admin.register(TipoEquipo)
class TipoEquipoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'departamento', 'fecha_creacion']
    list_filter = ['departamento']
    search_fields = ['nombre', 'descripcion']


@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'tipo_equipo', 'estado', 'fecha_adquisicion']
    list_filter = ['estado', 'tipo_equipo']
    search_fields = ['nombre', 'codigo']
    readonly_fields = ['imagen']
