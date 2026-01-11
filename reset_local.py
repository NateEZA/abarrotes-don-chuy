from app import app, db, Usuario
import os

DB_NAME = 'abarrotes_don_chuy.db'

print("🛠️  REINICIANDO BASE DE DATOS...")

# 1. Borrar la base de datos actual para evitar errores
if os.path.exists(DB_NAME):
    os.remove(DB_NAME)
    print("🗑️  Base de datos vieja eliminada.")

with app.app_context():
    # 2. Crear tablas limpias
    db.create_all()
    print("✅  Tablas creadas.")

    # 3. Crear el ADMIN con contraseña SEGURA
    # Nota: Usamos 'Admin123!' (A mayúscula, números y !)
    admin = Usuario(
        nombre_usuario='Admin',
        email='admin@abarrotes.com',
        rol='Admin',
        palabra_clave='admin123'
    )
    admin.establecer_contrasena('Admin123!') 
    
    db.session.add(admin)
    db.session.commit()
    print("👤  Usuario 'Admin' creado exitosamente.")

print("🚀  ¡LISTO! Ahora sí puedes iniciar sesión.")