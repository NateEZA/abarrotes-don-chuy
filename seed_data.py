from app import app, db
from models import Usuario, Producto, Orden, ItemOrden, Direccion, MetodoPago, Resena

def inicializar_db():
    with app.app_context():
        # Eliminar todas las tablas y recrearlas
        db.drop_all()
        db.create_all()
        
        print("="*60)
        print("Base de datos creada exitosamente")
        print("="*60)
        
        # Crear usuario Super Admin "Nate"
        nate = Usuario(
            nombre_usuario='Nate',
            email='nate@abarrotesdonchuy.com',
            rol='Admin',
            palabra_clave='mi primera mascota'
        )
        nate.establecer_contrasena('Nate123!')
        db.session.add(nate)
        
        # Crear un administrador regular
        admin = Usuario(
            nombre_usuario='admin',
            email='admin@abarrotesdonchuy.com',
            rol='Admin',
            palabra_clave='ciudad natal'
        )
        admin.establecer_contrasena('Admin123!')
        db.session.add(admin)
        
        # Crear vendedores de prueba
        vendedor1 = Usuario(
            nombre_usuario='maria_gomez',
            email='maria@abarrotesdonchuy.com',
            rol='Vendedor',
            palabra_clave='color favorito'
        )
        vendedor1.establecer_contrasena('Vende123!')
        db.session.add(vendedor1)
        
        vendedor2 = Usuario(
            nombre_usuario='juan_perez',
            email='juan@abarrotesdonchuy.com',
            rol='Vendedor',
            palabra_clave='comida favorita'
        )
        vendedor2.establecer_contrasena('Vende123!')
        db.session.add(vendedor2)
        
        # Crear compradores de prueba
        comprador1 = Usuario(
            nombre_usuario='carlos_lopez',
            email='carlos@cliente.com',
            rol='Comprador',
            palabra_clave='nombre de madre'
        )
        comprador1.establecer_contrasena('Compra123!')
        db.session.add(comprador1)
        
        comprador2 = Usuario(
            nombre_usuario='ana_martinez',
            email='ana@cliente.com',
            rol='Comprador',
            palabra_clave='mejor amigo'
        )
        comprador2.establecer_contrasena('Compra123!')
        db.session.add(comprador2)
        
        db.session.commit()
        print("\n✓ Usuarios creados exitosamente")
        
        # Crear productos electrónicos
        productos = [
            {
                'nombre': 'iPhone 15 Pro Max 256GB',
                'descripcion': 'Smartphone Apple con chip A17 Pro, cámara de 48MP, pantalla Super Retina XDR de 6.7 pulgadas, iOS 17',
                'precio': 28999.00,
                'stock': 15,
                'id_vendedor': vendedor1.id,
                'esta_aprobado': True
            },
            {
                'nombre': 'Samsung Galaxy S24 Ultra',
                'descripcion': 'Smartphone Samsung con Snapdragon 8 Gen 3, 12GB RAM, 256GB almacenamiento, S Pen integrado',
                'precio': 26999.00,
                'stock': 20,
                'id_vendedor': vendedor1.id,
                'esta_aprobado': True
            },
            {
                'nombre': 'MacBook Pro 14" M3',
                'descripcion': 'Laptop Apple con chip M3, 16GB RAM, SSD 512GB, pantalla Liquid Retina XDR, macOS Sonoma',
                'precio': 45999.00,
                'stock': 8,
                'id_vendedor': vendedor2.id,
                'esta_aprobado': True
            },
            {
                'nombre': 'Dell XPS 15',
                'descripcion': 'Laptop Dell con Intel Core i7 13va Gen, 16GB RAM, SSD 1TB, NVIDIA RTX 4050, pantalla 15.6" OLED',
                'precio': 38999.00,
                'stock': 12,
                'id_vendedor': vendedor2.id,
                'esta_aprobado': False  # Pendiente de aprobación
            },
            {
                'nombre': 'iPad Pro 12.9" M2',
                'descripcion': 'Tablet Apple con chip M2, 256GB, pantalla Liquid Retina XDR, compatible con Apple Pencil',
                'precio': 24999.00,
                'stock': 10,
                'id_vendedor': vendedor1.id,
                'esta_aprobado': True
            },
            {
                'nombre': 'AirPods Pro 2da Gen',
                'descripcion': 'Audífonos inalámbricos Apple con cancelación activa de ruido, audio espacial, chip H2',
                'precio': 5499.00,
                'stock': 30,
                'id_vendedor': vendedor2.id,
                'esta_aprobado': True
            },
            {
                'nombre': 'Sony WH-1000XM5',
                'descripcion': 'Audífonos over-ear con cancelación de ruido premium, 30 horas de batería, audio Hi-Res',
                'precio': 7999.00,
                'stock': 25,
                'id_vendedor': vendedor1.id,
                'esta_aprobado': True
            },
            {
                'nombre': 'Samsung Galaxy Watch 6',
                'descripcion': 'Smartwatch con pantalla Super AMOLED, GPS, monitoreo de salud 24/7, resistente al agua',
                'precio': 6999.00,
                'stock': 18,
                'id_vendedor': vendedor2.id,
                'esta_aprobado': True
            },
            {
                'nombre': 'Xiaomi 13T Pro 5G',
                'descripcion': 'Smartphone con MediaTek Dimensity 9200+, 12GB RAM, cámara Leica de 50MP, carga rápida 120W',
                'precio': 13999.00,
                'stock': 22,
                'id_vendedor': vendedor1.id,
                'esta_aprobado': True
            },
            {
                'nombre': 'Lenovo Legion 5 Pro',
                'descripcion': 'Laptop gaming con AMD Ryzen 7, RTX 4060 8GB, 16GB RAM, SSD 1TB, pantalla 165Hz QHD',
                'precio': 32999.00,
                'stock': 6,
                'id_vendedor': vendedor2.id,
                'esta_aprobado': True
            },
            {
                'nombre': 'Nintendo Switch OLED',
                'descripcion': 'Consola híbrida con pantalla OLED de 7 pulgadas, 64GB almacenamiento, Joy-Con incluidos',
                'precio': 8499.00,
                'stock': 14,
                'id_vendedor': vendedor1.id,
                'esta_aprobado': True
            },
            {
                'nombre': 'PlayStation 5',
                'descripcion': 'Consola de videojuegos con SSD ultra rápido, ray tracing, 4K hasta 120fps, control DualSense',
                'precio': 14999.00,
                'stock': 5,
                'id_vendedor': vendedor2.id,
                'esta_aprobado': True
            }
        ]
        
        for prod_data in productos:
            producto = Producto(**prod_data)
            db.session.add(producto)
        
        db.session.commit()
        print("✓ Productos electrónicos creados exitosamente")
        
        # Crear direcciones para compradores
        direccion1 = Direccion(
            id_usuario=comprador1.id,
            calle='Av. Insurgentes Sur 1234',
            ciudad='Ciudad de México',
            estado='CDMX',
            codigo_postal='03100',
            pais='México',
            es_predeterminada=True
        )
        db.session.add(direccion1)
        
        direccion2 = Direccion(
            id_usuario=comprador1.id,
            calle='Calle Reforma 456, Col. Juárez',
            ciudad='Ciudad de México',
            estado='CDMX',
            codigo_postal='06600',
            pais='México',
            es_predeterminada=False
        )
        db.session.add(direccion2)
        
        direccion3 = Direccion(
            id_usuario=comprador2.id,
            calle='Av. Chapultepec 789',
            ciudad='Guadalajara',
            estado='Jalisco',
            codigo_postal='44100',
            pais='México',
            es_predeterminada=True
        )
        db.session.add(direccion3)
        
        db.session.commit()
        print("✓ Direcciones creadas exitosamente")
        
        # Crear métodos de pago
        from datetime import datetime
        anio_actual = datetime.now().year % 100
        
        pago1 = MetodoPago(
            id_usuario=comprador1.id,
            ultimos4_tarjeta='1234',
            titular_tarjeta='CARLOS LOPEZ GARCIA',
            mes_vencimiento=12,
            anio_vencimiento=anio_actual + 2,
            es_predeterminado=True
        )
        db.session.add(pago1)
        
        pago2 = MetodoPago(
            id_usuario=comprador2.id,
            ultimos4_tarjeta='5678',
            titular_tarjeta='ANA MARTINEZ LOPEZ',
            mes_vencimiento=6,
            anio_vencimiento=anio_actual + 3,
            es_predeterminado=True
        )
        db.session.add(pago2)
        
        db.session.commit()
        print("✓ Métodos de pago creados exitosamente")
        
        # Crear órdenes de ejemplo
        orden1 = Orden(
            id_comprador=comprador1.id,
            total=34498.00,
            estado='Completada',
            id_direccion_envio=direccion1.id,
            id_metodo_pago=pago1.id
        )
        db.session.add(orden1)
        db.session.flush()
        
        # Items de la orden 1
        item1 = ItemOrden(
            id_orden=orden1.id,
            id_producto=1,  # iPhone 15 Pro Max
            cantidad=1,
            precio=28999.00
        )
        db.session.add(item1)
        
        item2 = ItemOrden(
            id_orden=orden1.id,
            id_producto=6,  # AirPods Pro
            cantidad=1,
            precio=5499.00
        )
        db.session.add(item2)
        
        # Orden 2
        orden2 = Orden(
            id_comprador=comprador2.id,
            total=45999.00,
            estado='Completada',
            id_direccion_envio=direccion3.id,
            id_metodo_pago=pago2.id
        )
        db.session.add(orden2)
        db.session.flush()
        
        item3 = ItemOrden(
            id_orden=orden2.id,
            id_producto=3,  # MacBook Pro
            cantidad=1,
            precio=45999.00
        )
        db.session.add(item3)
        
        db.session.commit()
        print("✓ Órdenes creadas exitosamente")
        
        # Crear reseñas
        resena1 = Resena(
            id_usuario=comprador1.id,
            id_producto=1,  # iPhone
            calificacion=5,
            comentario='Excelente teléfono, la cámara es increíble y la batería dura todo el día'
        )
        db.session.add(resena1)
        
        resena2 = Resena(
            id_usuario=comprador1.id,
            id_producto=6,  # AirPods
            calificacion=5,
            comentario='Mejor cancelación de ruido que he probado, perfectos para trabajar'
        )
        db.session.add(resena2)
        
        resena3 = Resena(
            id_usuario=comprador2.id,
            id_producto=3,  # MacBook
            calificacion=5,
            comentario='Potencia increíble, la pantalla es hermosa. Vale cada peso'
        )
        db.session.add(resena3)
        
        db.session.commit()
        print("✓ Reseñas creadas exitosamente")
        
        print("\n" + "="*60)
        print("✓✓✓ DATOS DE PRUEBA CREADOS EXITOSAMENTE ✓✓✓")
        print("="*60)
        print("\n🏪 BIENVENIDO A ABARROTES DON CHUY 🏪")
        print("Tienda de Electrónica y Tecnología")
        print("\nCREDENCIALES DE ACCESO:")
        print("-" * 60)
        print("\n👑 Super Administrador:")
        print("  Usuario: Nate")
        print("  Contraseña: Nate123!")
        print("  Palabra clave: mi primera mascota")
        print("\n🔧 Administrador Regular:")
        print("  Usuario: admin")
        print("  Contraseña: Admin123!")
        print("  Palabra clave: ciudad natal")
        print("\n🏪 Vendedor 1:")
        print("  Usuario: maria_gomez")
        print("  Contraseña: Vende123!")
        print("  Palabra clave: color favorito")
        print("\n🏪 Vendedor 2:")
        print("  Usuario: juan_perez")
        print("  Contraseña: Vende123!")
        print("  Palabra clave: comida favorita")
        print("\n🛒 Comprador 1:")
        print("  Usuario: carlos_lopez")
        print("  Contraseña: Compra123!")
        print("  Palabra clave: nombre de madre")
        print("\n🛒 Comprador 2:")
        print("  Usuario: ana_martinez")
        print("  Contraseña: Compra123!")
        print("  Palabra clave: mejor amigo")
        print("\n" + "="*60)
        print("📦 Base de datos: abarrotes_don_chuy.db")
        print("🌐 Ejecuta: python app.py")
        print("🔗 Accede a: http://127.0.0.1:5000")
        print("="*60)

if __name__ == '__main__':
    inicializar_db()