from django.db import models


class Departamento(models.TextChoices):
    GENERAL = 'GENERAL', 'General'
    SISTEMAS = 'SISTEMAS', 'Sistemas'
    CONTABILIDAD = 'CONTABILIDAD', 'Contabilidad'
    LOGISTICA = 'LOGISTICA', 'Logística'
    OPERACIONES = 'OPERACIONES', 'Operaciones'


class TipoEquipo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    departamento = models.CharField(
        max_length=50, choices=Departamento.choices, default=Departamento.GENERAL
    )

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Tipo de Equipo"
        verbose_name_plural = "Tipos de Equipos"
        ordering = ['nombre']

class Equipo(models.Model):
    ESTADO_CHOICES = [
        ('disponible', 'Disponible'),
        ('prestado', 'Prestado'),
        ('mantenimiento', 'En Mantenimiento'),
        ('daniado', 'Dañado'),
    ]

    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=50, unique=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='disponible')
    imagen = models.ImageField(
        upload_to='equipos_img/',
        blank=True, null=True,
    )

    tipo_equipo = models.ForeignKey(
        TipoEquipo, on_delete=models.PROTECT, related_name='equipos'
    )
    
    # Campo extra para cumplir requisitos
    fecha_adquisicion = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    class Meta:
        ordering = ['codigo']
        verbose_name = "Equipo"
        verbose_name_plural = "Equipos"
    