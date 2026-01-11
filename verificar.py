from app import app, Usuario

print("🕵️‍♂️  INVESTIGANDO CREDENCIALES...")

with app.app_context():
    # 1. Buscamos si el usuario existe
    user = Usuario.query.filter_by(nombre_usuario='Admin').first()
    
    if not user:
        print("❌ ERROR GRAVE: El usuario 'Admin' NO EXISTE en la base de datos.")
        print("   -> Solución: Ejecuta 'python reset_local.py' de nuevo.")
    else:
        print(f"✅ El usuario '{user.nombre_usuario}' sí existe.")
        
        # 2. Probamos la contraseña 'Admin123!'
        password_prueba = 'Admin123!'
        es_valida = user.verificar_contrasena(password_prueba)
        
        if es_valida:
            print(f"✅ La contraseña '{password_prueba}' es CORRECTA.")
            print("   -> Si no puedes entrar en la web, verifica que escribes 'Admin' con A mayúscula.")
        else:
            print(f"❌ La contraseña '{password_prueba}' es INCORRECTA.")
            print("   -> Probablemente se guardó una versión vieja o diferente.")