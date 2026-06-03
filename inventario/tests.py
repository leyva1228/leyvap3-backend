import tempfile

from django.test import TestCase, override_settings
from PIL import Image
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Departamento, Equipo, TipoEquipo


class TipoEquipoAPITest(APITestCase):
    def test_list_tipos(self):
        TipoEquipo.objects.create(nombre="Laptop", descripcion="Equipos portátiles")
        response = self.client.get('/api/tipos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_tipo(self):
        data = {
            'nombre': 'Monitor',
            'descripcion': 'Pantallas y monitores',
            'departamento': Departamento.SISTEMAS,
        }
        response = self.client.post('/api/tipos/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['nombre'], 'Monitor')

    def test_create_tipo_default_departamento(self):
        data = {'nombre': 'Teclado', 'descripcion': 'Teclados y periféricos'}
        response = self.client.post('/api/tipos/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['departamento'], Departamento.GENERAL)

    def test_update_tipo(self):
        tipo = TipoEquipo.objects.create(nombre="Laptop", descripcion="Portátiles")
        response = self.client.patch(f'/api/tipos/{tipo.pk}/', {'nombre': 'Laptop Gamer'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], 'Laptop Gamer')

    def test_delete_tipo(self):
        tipo = TipoEquipo.objects.create(nombre="Tablet", descripcion="Tablets")
        response = self.client.delete(f'/api/tipos/{tipo.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_search_tipo_by_nombre(self):
        TipoEquipo.objects.create(nombre="Laptop", descripcion="Portátil")
        TipoEquipo.objects.create(nombre="Monitor", descripcion="Pantalla")
        response = self.client.get('/api/tipos/?search=Laptop')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)


class EquipoAPITest(APITestCase):
    def setUp(self):
        self.tipo = TipoEquipo.objects.create(
            nombre="Laptop", descripcion="Equipos portátiles"
        )

    def test_list_equipos(self):
        Equipo.objects.create(
            nombre="HP Probook", codigo="EQ-001", tipo_equipo=self.tipo
        )
        response = self.client.get('/api/equipos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_equipo(self):
        data = {
            'nombre': 'Dell Latitude',
            'codigo': 'EQ-002',
            'tipo_equipo': self.tipo.pk,
        }
        response = self.client.post('/api/equipos/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['nombre'], 'Dell Latitude')

    def test_create_equipo_sin_tipo_falla(self):
        data = {'nombre': 'Sin Tipo', 'codigo': 'EQ-003'}
        response = self.client.post('/api/equipos/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_equipo_serializer_incluye_tipo_nombre(self):
        equipo = Equipo.objects.create(
            nombre="MacBook Pro", codigo="EQ-004", tipo_equipo=self.tipo
        )
        response = self.client.get(f'/api/equipos/{equipo.pk}/')
        self.assertEqual(response.data['tipo_equipo_nombre'], 'Laptop')

    def test_protect_delete_tipo_con_equipos(self):
        Equipo.objects.create(
            nombre="Lenovo ThinkPad", codigo="EQ-005", tipo_equipo=self.tipo
        )
        response = self.client.delete(f'/api/tipos/{self.tipo.pk}/')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertIn('equipos asociados', response.json()['error'])
        self.assertTrue(TipoEquipo.objects.filter(pk=self.tipo.pk).exists())

    def test_search_equipo_by_codigo(self):
        Equipo.objects.create(
            nombre="HP Probook", codigo="EQ-001", tipo_equipo=self.tipo
        )
        Equipo.objects.create(
            nombre="Dell Latitude", codigo="EQ-002", tipo_equipo=self.tipo
        )
        response = self.client.get('/api/equipos/?search=EQ-001')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_estado_default_disponible(self):
        equipo = Equipo.objects.create(
            nombre="Asus ZenBook", codigo="EQ-006", tipo_equipo=self.tipo
        )
        self.assertEqual(equipo.estado, 'disponible')

    def test_update_estado_equipo(self):
        equipo = Equipo.objects.create(
            nombre="Acer Swift", codigo="EQ-007", tipo_equipo=self.tipo
        )
        response = self.client.patch(
            f'/api/equipos/{equipo.pk}/', {'estado': 'prestado'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['estado'], 'prestado')

    def test_delete_equipo(self):
        equipo = Equipo.objects.create(
            nombre="Xiaomi Book", codigo="EQ-008", tipo_equipo=self.tipo
        )
        response = self.client.delete(f'/api/equipos/{equipo.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_codigo_unico(self):
        Equipo.objects.create(
            nombre="HP EliteBook", codigo="EQ-009", tipo_equipo=self.tipo
        )
        data = {
            'nombre': 'HP EliteBook Duplicate',
            'codigo': 'EQ-009',
            'tipo_equipo': self.tipo.pk,
        }
        response = self.client.post('/api/equipos/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class EquipoModelTest(TestCase):
    def setUp(self):
        self.tipo = TipoEquipo.objects.create(
            nombre="Impresora", descripcion="Impresoras láser"
        )

    def test_str_representation(self):
        equipo = Equipo.objects.create(
            nombre="HP LaserJet", codigo="IMP-001", tipo_equipo=self.tipo
        )
        self.assertEqual(str(equipo), "IMP-001 - HP LaserJet")

    def test_tipo_str_representation(self):
        self.assertEqual(str(self.tipo), "Impresora")


class ImageValidationTest(APITestCase):
    @override_settings(MEDIA_ROOT=tempfile.mkdtemp())
    def test_subir_imagen_valida(self):
        tipo = TipoEquipo.objects.create(nombre="Laptop", descripcion="Portátiles")
        img = Image.new('RGB', (100, 100), color='red')
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            img.save(tmp.name)
            with open(tmp.name, 'rb') as f:
                response = self.client.post('/api/equipos/', {
                    'nombre': 'Laptop con Foto',
                    'codigo': 'EQ-FOTO',
                    'tipo_equipo': tipo.pk,
                    'imagen': f,
                })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('imagen', response.data)
