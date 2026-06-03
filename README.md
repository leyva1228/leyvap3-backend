# LeyvaP3 - Backend (Django REST API)

**Práctica Calificada N°3 — Desarrollo de Aplicaciones Empresariales**

| | |
|---|---|
| **Institución** | Instituto Privado TECSUP Trujillo — Campus Norte |
| **Carrera** | C-24 Diseño y Desarrollo de Software |
| **Ciclo** | 4to ciclo — 2026 |
| **Curso** | Desarrollo de Aplicaciones Empresariales |
| **Tema** | Sistema de Inventario de Laboratorio |

## Descripción

API REST desarrollada con **Django + Django Rest Framework** para gestionar un inventario de laboratorio. Contiene dos modelos relacionados mediante clave foránea: **Categorías** y **Equipos**, cada uno con al menos 4 campos incluyendo un campo de tipo imagen. El frontend en **React** consume esta API.

## Stack

- **Django 5** con Django Rest Framework
- **PostgreSQL** como base de datos (alojada en Render)
- **Cloudinary** para almacenamiento de imágenes
- Desplegado en **Render** via Gunicorn

## Modelos

### Categoría
- `id`, `nombre`, `descripcion`, `fecha_creacion`

### Equipo
- `id`, `nombre`, `descripcion`, `categoria` (FK), `imagen`, `cantidad`, `fecha_registro`

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/categorias/` | Listar categorías |
| POST | `/api/categorias/` | Crear categoría |
| GET | `/api/categorias/:id/` | Detalle de categoría |
| PUT | `/api/categorias/:id/` | Actualizar categoría |
| DELETE | `/api/categorias/:id/` | Eliminar categoría |
| GET | `/api/equipos/` | Listar equipos |
| POST | `/api/equipos/` | Crear equipo |
| GET | `/api/equipos/:id/` | Detalle de equipo |
| PUT | `/api/equipos/:id/` | Actualizar equipo |
| DELETE | `/api/equipos/:id/` | Eliminar equipo |

## Enlaces

- **Backend (Render):** https://leyvap3-backend.onrender.com
- **Frontend (Vercel):** https://leyvap3-frontend.vercel.app
