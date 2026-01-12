# 🏪 Abarrotes Don Chuy - Sistema E-Commerce

Sistema completo de comercio electrónico desarrollado con Flask, implementando control de acceso basado en roles (RBAC) para una tienda de abarrotes mexicana.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🌟 Características

- ✅ Sistema de roles: Admin, Vendedor, Comprador
- ✅ Autenticación y autorización segura
- ✅ Gestión completa de productos
- ✅ Carrito de compras funcional
- ✅ Sistema de reseñas y calificaciones
- ✅ Panel de administración
- ✅ Validaciones de seguridad
- ✅ Diseño responsive

## 🚀 Instalación Rápida

### 1. Clonar el repositorio
```bash
git clone https://github.com/TU-USUARIO/abarrotes-don-chuy.git
cd abarrotes-don-chuy
```

### 2. Crear entorno virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Inicializar base de datos
```bash
python seed_data.py
```

### 5. Ejecutar aplicación
```bash
python app.py
```

### 6. Abrir en navegador
```
http://127.0.0.1:5000
```

## 🔑 Credenciales de Acceso

| Rol | Usuario | Contraseña |
|-----|---------|------------|
| Super Admin | Nate | Nate123! |
| Admin | admin | Admin123! |
| Vendedor | maria_gomez | Vende123! |
| Vendedor | juan_perez | Vende123! |
| Comprador | carlos_lopez | Compra123! |
| Comprador | ana_martinez | Compra123! |

## 📦 Tecnologías

- **Backend:** Flask 3.0
- **Base de Datos:** SQLite con SQLAlchemy
- **Frontend:** HTML5, CSS3, Jinja2
- **Seguridad:** Werkzeug (hashing de contraseñas)

## 📂 Estructura del Proyecto
```
abarrotes-don-chuy/
│
├── app.py                    # Aplicación Flask principal
├── models.py                 # Modelos de base de datos
├── seed_data.py              # Datos de inicialización
├── requirements.txt          # Dependencias
│
├── templates/                # Plantillas HTML
│   ├── base.html
│   ├── index.html
│   └── ...
│
└── static/
    └── uploads/              # Imágenes de productos
```

## 👥 Roles y Permisos

### 👑 Administrador
- Ver estadísticas globales
- Gestionar usuarios
- Aprobar productos de vendedores
- Ver historial de todas las ventas

### 🏪 Vendedor
- CRUD de productos propios
- Subir imágenes de productos
- Ver estadísticas de ventas propias
- Gestionar inventario

### 🛒 Comprador
- Navegar catálogo
- Carrito de compras
- Proceso de checkout completo
- Dejar reseñas (solo productos comprados)
- Historial de compras

## 🔒 Seguridad

- ✅ Contraseñas hasheadas con Werkzeug
- ✅ Validación de contraseña (8+ caracteres, número, símbolo)
- ✅ Sesiones seguras
- ✅ Validación de permisos por rol
- ✅ Validación de tarjetas (fecha, CVV)

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

## 👨‍💻 Autor

[Nathan y Efrain] - [Tu GitHub](https://github.com/NateEZA)

---

⭐ Si te gusta este proyecto, dale una estrella en GitHub!