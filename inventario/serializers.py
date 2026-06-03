from rest_framework import serializers
from .models import TipoEquipo, Equipo

class TipoEquipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoEquipo
        fields = '__all__'

class EquipoSerializer(serializers.ModelSerializer):
    tipo_equipo_nombre = serializers.CharField(source='tipo_equipo.nombre', read_only=True)

    class Meta:
        model = Equipo
        fields = ['id', 'nombre', 'codigo', 'estado', 'imagen', 'tipo_equipo',
                  'tipo_equipo_nombre', 'fecha_adquisicion']
        