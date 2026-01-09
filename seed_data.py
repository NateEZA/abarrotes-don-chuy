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
            rol='Admin'
        )
        nate.establecer_contrasena('Nate123!')  # Cumple con requisitos: 8 chars, número, símbolo
        db.session.add(nate)
        
        # Crear un administrador regular
        admin = Usuario(
            nombre_usuario='admin',
            email='admin@abarrotesdonchuy.com',
            rol='Admin'
        )
        admin.establecer_contrasena('Admin123!')
        db.session.add(admin)
        
        # Crear vendedores de prueba
        vendedor1 = Usuario(
            nombre_usuario='maria_gomez',
            email='maria@abarrotesdonchuy.com',
            rol='Vendedor'
        )
        vendedor1.establecer_contrasena('Vende123!')
        db.session.add(vendedor1)
        
        vendedor2 = Usuario(
            nombre_usuario='juan_perez',
            email='juan@abarrotesdonchuy.com',
            rol='Vendedor'
        )
        vendedor2.establecer_contrasena('Vende123!')
        db.session.add(vendedor2)
        
        # Crear compradores de prueba
        comprador1 = Usuario(
            nombre_usuario='carlos_lopez',
            email='carlos@cliente.com',
            rol='Comprador'
        )
        comprador1.establecer_contrasena('Compra123!')
        db.session.add(comprador1)
        
        comprador2 = Usuario(
            nombre_usuario='ana_martinez',
            email='ana@cliente.com',
            rol='Comprador'
        )
        comprador2.establecer_contrasena('Compra123!')
        db.session.add(comprador2)
        
        db.session.commit()
        print("\n✓ Usuarios creados exitosamente")
        
        # Crear productos de prueba típicos de abarrotes
        productos = [
            {
                'nombre': 'Aceite Vegetal 1L',
                'descripcion': 'Aceite vegetal comestible 100% puro, ideal para cocinar y freír',
                'precio': 45.50,
                'stock': 50,
                'id_vendedor': vendedor1.id,
                'esta_aprobado': True
            },
            {
                'nombre': 'Arroz Blanco 1kg',
                'descripcion': 'Arroz blanco de grano largo, calidad premium',
                'precio': 28.00,
                'stock': 100,
                'id_vendedor': vendedor1.id,
                'esta_aprobado': True
            },
            {
                'nombre': 'Frijol Negro 1kg',
                'descripcion': 'Frijol negro seleccionado, rico en proteínas',
                'precio': 35.00,
                'stock': 75,
                'id_vendedor': vendedor2.id,
                'esta_aprobado': True
            },
            {
                'nombre': 'Azúcar Refinada 2kg',
                'descripcion': 'Azúcar blanca refinada, endulzante natural',
                'precio': 38.50,
                'stock': 60,
                'id_vendedor': vendedor2.id,
                'esta_aprobado': False  # Pendiente de aprobación
            },
            {
                'nombre': 'Café Molido 500g',
                'descripcion': 'Café 100% arabica, molido medio, sabor intenso',
                'precio': 125.00,
                'stock': 30,
                'id_vendedor': vendedor1.id,
                'esta_aprobado': True
            },
            {
                'nombre': 'Pasta Espagueti 500g',
                'descripcion': 'Pasta de trigo duro, cocción rápida',
                'precio': 22.50,
                'stock': 80,
                'id_vendedor': vendedor2.id,
                'esta_aprobado': True
            },
            {
                'nombre': 'Harina de Trigo 1kg',
                'descripcion': 'Harina refinada para todo uso, ideal para panificación',
                'precio': 25.00,
                'stock': 90,
                'id_vendedor': vendedor1.id,
                'esta_aprobado': True
            },
            {
                'nombre': 'Sal de Mesa 1kg',
                'descripcion': 'Sal refinada yodada, indispensable en tu cocina',
                'precio': 12.00,
                'stock': 120,
                'id_vendedor': vendedor2.id,
                'esta_aprobado': True
            },
            {
                'nombre': 'Atún en Lata 140g',
                'descripcion': 'Atún en agua, alto contenido de proteína',
                'precio': 18.50,
                'stock': 150,
                'id_vendedor': vendedor1.id,
                'esta_aprobado': True
            },
            {
                'nombre': 'Leche Entera 1L',
                'descripcion': 'Leche entera pasteurizada, rica en calcio',
                'precio': 22.00,
                'stock': 40,
                'id_vendedor': vendedor2.id,
                'esta_aprobado': True
            }
        ]
        
        for prod_data in productos:
            producto = Producto(**prod_data)
            db.session.add(producto)
        
        db.session.commit()
        print("✓ Productos creados exitosamente")
        
        # Crear direcciones para compradores
        direccion1 = Direccion(
            id_usuario=comprador1.id,
            calle='Av. Juárez 123, Col. Centro',
            ciudad='Ciudad de México',
            estado='CDMX',
            codigo_postal='06000',
            pais='México',
            es_predeterminada=True
        )
        db.session.add(direccion1)
        
        direccion2 = Direccion(
            id_usuario=comprador1.id,
            calle='Calle Reforma 456, Col. Polanco',
            ciudad='Ciudad de México',
            estado='CDMX',
            codigo_postal='11560',
            pais='México',
            es_predeterminada=False
        )
        db.session.add(direccion2)
        
        direccion3 = Direccion(
            id_usuario=comprador2.id,
            calle='Insurgentes Sur 789, Col. Del Valle',
            ciudad='Ciudad de México',
            estado='CDMX',
            codigo_postal='03100',
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
            total=193.50,
            estado='Completada',
            id_direccion_envio=direccion1.id,
            id_metodo_pago=pago1.id
        )
        db.session.add(orden1)
        db.session.flush()
        
        # Items de la orden 1
        item1 = ItemOrden(
            id_orden=orden1.id,
            id_producto=1,  # Aceite
            cantidad=2,
            precio=45.50
        )
        db.session.add(item1)
        
        item2 = ItemOrden(
            id_orden=orden1.id,
            id_producto=3,  # Frijol
            cantidad=3,
            precio=35.00
        )
        db.session.add(item2)
        
        # Orden 2
        orden2 = Orden(
            id_comprador=comprador2.id,
            total=147.50,
            estado='Completada',
            id_direccion_envio=direccion3.id,
            id_metodo_pago=pago2.id
        )
        db.session.add(orden2)
        db.session.flush()
        
        item3 = ItemOrden(
            id_orden=orden2.id,
            id_producto=5,  # Café
            cantidad=1,
            precio=125.00
        )
        db.session.add(item3)
        
        item4 = ItemOrden(
            id_orden=orden2.id,
            id_producto=6,  # Pasta
            cantidad=1,
            precio=22.50
        )
        db.session.add(item4)
        
        db.session.commit()
        print("✓ Órdenes creadas exitosamente")
        
        # Crear reseñas
        resena1 = Resena(
            id_usuario=comprador1.id,
            id_producto=1,  # Aceite
            calificacion=5,
            comentario='Excelente aceite, muy buena calidad y precio justo'
        )
        db.session.add(resena1)
        
        resena2 = Resena(
            id_usuario=comprador1.id,
            id_producto=3,  # Frijol
            calificacion=4,
            comentario='Buenos frijoles, aunque tardaron un poco más en cocinarse'
        )
        db.session.add(resena2)
        
        resena3 = Resena(
            id_usuario=comprador2.id,
            id_producto=5,  # Café
            calificacion=5,
            comentario='El mejor café que he probado, aroma increíble'
        )
        db.session.add(resena3)
        
        resena4 = Resena(
            id_usuario=comprador2.id,
            id_producto=6,  # Pasta
            calificacion=4,
            comentario='Buena pasta, se cocina rápido y tiene buen sabor'
        )
        db.session.add(resena4)
        
        db.session.commit()
        print("✓ Reseñas creadas exitosamente")
        
        print("\n" + "="*60)
        print("✓✓✓ DATOS DE PRUEBA CREADOS EXITOSAMENTE ✓✓✓")
        print("="*60)
        print("\n🏪 BIENVENIDO A ABARROTES DON CHUY 🏪")
        print("\nCREDENCIALES DE ACCESO:")
        print("-" * 60)
        print("\n👑 Super Administrador (Puede crear otros admins):")
        print("  Usuario: Nate")
        print("  Contraseña: Nate123!")
        print("\n🔧 Administrador Regular:")
        print("  Usuario: admin")
        print("  Contraseña: Admin123!")
        print("\n🏪 Vendedor 1:")
        print("  Usuario: maria_gomez")
        print("  Contraseña: Vende123!")
        print("\n🏪 Vendedor 2:")
        print("  Usuario: juan_perez")
        print("  Contraseña: Vende123!")
        print("\n🛒 Comprador 1:")
        print("  Usuario: carlos_lopez")
        print("  Contraseña: Compra123!")
        print("\n🛒 Comprador 2:")
        print("  Usuario: ana_martinez")
        print("  Contraseña: Compra123!")
        print("\n" + "="*60)
        print("📦 Base de datos: abarrotes_don_chuy.db")
        print("🌐 Ejecuta: python app.py")
        print("🔗 Accede a: http://127.0.0.1:5000")
        print("="*60)

if __name__ == '__main__':
    inicializar_db()