from app import app, db
from models import Usuario
import os

print("☢️  INICIANDO REINSTALACIÓN DE BASE DE DATOS...")

# Borramos el archivo físico si existe para asegurar limpieza total
if os.path.exists('abarrotes_don_chuy.db'):
    os.remove('abarrotes_don_chuy.db')
    print("🗑️  Archivo de base de datos eliminado.")

with app.app_context():
    # Crea las tablas nuevas basadas en tus modelos actuales
    db.create_all()
    print("✅  Tablas creadas desde cero.")

    # Crea el Super Admin
    print("👤  Creando usuario Administrador...")
    admin = Usuario(
        nombre_usuario='Admin',
        email='admin@abarrotes.com',
        rol='Admin',
        palabra_clave='admin123'  # Clave de recuperación
    )
    admin.establecer_contrasena('admin123')
    
    db.session.add(admin)
    db.session.commit()
    print("✅  ¡Admin creado! Usuario: 'Admin' / Pass: 'admin123'")

print("🚀  ¡SISTEMA LISTO!")