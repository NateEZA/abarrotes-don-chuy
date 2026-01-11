from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from models import db, Usuario, Producto, Orden, ItemOrden, Direccion, MetodoPago, Resena
from werkzeug.utils import secure_filename
import os
import re
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abarrotes_don_chuy_clave_secreta_2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///abarrotes_don_chuy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB máximo

EXTENSIONES_PERMITIDAS = {'png', 'jpg', 'jpeg', 'gif'}

db.init_app(app)

# ============== UTILIDADES ==============

def archivo_permitido(nombre_archivo):
    return '.' in nombre_archivo and nombre_archivo.rsplit('.', 1)[1].lower() in EXTENSIONES_PERMITIDAS

def validar_contrasena(contrasena):
    if len(contrasena) < 8:
        return False, "La contraseña debe tener al menos 8 caracteres."
    if not re.search(r"[A-Z]", contrasena):
        return False, "La contraseña debe incluir al menos una letra MAYÚSCULA."
    if not re.search(r"\d", contrasena):
        return False, "La contraseña debe incluir al menos un número."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", contrasena):
        return False, "La contraseña debe incluir al menos un carácter especial (ej. ! @ # $)."
    return True, ""

def validar_vencimiento_tarjeta(mes, anio):
    try:
        mes = int(mes)
        anio = int(anio)
        
        if mes < 1 or mes > 12:
            return False, "Mes inválido (debe ser entre 01 y 12)"
        
        anio_actual = datetime.now().year % 100
        mes_actual = datetime.now().month
        
        if anio < anio_actual or (anio == anio_actual and mes < mes_actual):
            return False, "La tarjeta ha expirado"
        
        return True, ""
    except ValueError:
        return False, "Formato de fecha inválido"

def validar_cvv(cvv):
    return len(cvv) == 3 and cvv.isdigit()

# ============== DECORADORES ==============

def login_requerido(f):
    @wraps(f)
    def funcion_decorada(*args, **kwargs):
        if 'id_usuario' not in session:
            flash('Debes iniciar sesión para acceder a esta página', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return funcion_decorada

def rol_requerido(roles):
    def decorador(f):
        @wraps(f)
        def funcion_decorada(*args, **kwargs):
            if 'id_usuario' not in session:
                flash('Debes iniciar sesión', 'warning')
                return redirect(url_for('login'))
            
            usuario = Usuario.query.get(session['id_usuario'])
            if usuario.rol not in roles:
                flash('No tienes permisos para acceder a esta página', 'danger')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return funcion_decorada
    return decorador

# ============== RUTAS PÚBLICAS ==============

@app.route('/')
def index():
    productos = Producto.query.filter_by(esta_aprobado=True).all()
    return render_template('index.html', productos=productos)

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre_usuario = request.form.get('nombre_usuario')
        email = request.form.get('email')
        contrasena = request.form.get('contrasena')
        rol = request.form.get('rol', 'Comprador')
        # NUEVO: Obtener palabra clave
        palabra_clave = request.form.get('palabra_clave')
        
        # Validar que el usuario no exista
        if Usuario.query.filter_by(nombre_usuario=nombre_usuario).first():
            flash('El nombre de usuario ya existe', 'danger')
            return redirect(url_for('registro'))
        
        if Usuario.query.filter_by(email=email).first():
            flash('El correo electrónico ya está registrado', 'danger')
            return redirect(url_for('registro'))
        
        # Validar contraseña
        valido, mensaje = validar_contrasena(contrasena)
        if not valido:
            flash(mensaje, 'danger')
            return redirect(url_for('registro'))
        
        # Crear usuario (con palabra clave)
        usuario = Usuario(
            nombre_usuario=nombre_usuario, 
            email=email, 
            rol=rol,
            palabra_clave=palabra_clave # <-- GUARDAR CAMPO
        )
        usuario.establecer_contrasena(contrasena)
        
        db.session.add(usuario)
        db.session.commit()
        
        flash('¡Registro exitoso! Ahora puedes iniciar sesión', 'success')
        return redirect(url_for('login'))
    
    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nombre_usuario = request.form.get('nombre_usuario')
        contrasena = request.form.get('contrasena')
        
        usuario = Usuario.query.filter_by(nombre_usuario=nombre_usuario).first()
        
        if usuario and usuario.verificar_contrasena(contrasena):
            session['id_usuario'] = usuario.id
            session['nombre_usuario'] = usuario.nombre_usuario
            session['rol'] = usuario.rol
            flash(f'¡Bienvenido a Abarrotes Don Chuy, {usuario.nombre_usuario}!', 'success')
            
            if usuario.rol == 'Admin':
                return redirect(url_for('panel_admin'))
            elif usuario.rol == 'Vendedor':
                return redirect(url_for('panel_vendedor'))
            else:
                return redirect(url_for('index'))
        else:
            flash('Credenciales inválidas', 'danger')
    
    return render_template('login.html')

# --- NUEVA RUTA: RECUPERAR CONTRASEÑA ---
@app.route('/recuperar', methods=['GET', 'POST'])
def recuperar_password():
    if request.method == 'POST':
        email = request.form.get('email')
        palabra_clave_ingresada = request.form.get('palabra_clave')
        nueva_contrasena = request.form.get('nueva_contrasena')
        
        usuario = Usuario.query.filter_by(email=email).first()
        
        if not usuario:
            flash('El correo no está registrado.', 'danger')
            return redirect(url_for('recuperar_password'))
            
        # Verificar palabra clave (Coincidencia exacta)
        if usuario.palabra_clave != palabra_clave_ingresada:
            flash('La palabra clave es incorrecta.', 'danger')
            return redirect(url_for('recuperar_password'))
            
        # Validar la nueva contraseña
        valido, mensaje = validar_contrasena(nueva_contrasena)
        if not valido:
            flash(mensaje, 'danger')
            return redirect(url_for('recuperar_password'))
            
        # Actualizar contraseña
        usuario.establecer_contrasena(nueva_contrasena)
        db.session.commit()
        
        flash('¡Contraseña actualizada correctamente! Inicia sesión.', 'success')
        return redirect(url_for('login'))
        
    return render_template('recuperar.html')

@app.route('/cerrar-sesion')
def cerrar_sesion():
    session.clear()
    flash('Has cerrado sesión exitosamente', 'info')
    return redirect(url_for('index'))

# ============== RUTAS DE PRODUCTOS ==============

@app.route('/producto/<int:id_producto>')
def detalle_producto(id_producto):
    producto = Producto.query.get_or_404(id_producto)
    resenas = Resena.query.filter_by(id_producto=id_producto).all()
    
    # Verificar si el usuario ya compró este producto
    puede_resenar = False
    if 'id_usuario' in session:
        ordenes_usuario = Orden.query.filter_by(id_comprador=session['id_usuario']).all()
        for orden in ordenes_usuario:
            if any(item.id_producto == id_producto for item in orden.items):
                puede_resenar = True
                break
    
    return render_template('detalle_producto.html', producto=producto, resenas=resenas, puede_resenar=puede_resenar)

@app.route('/agregar-resena/<int:id_producto>', methods=['POST'])
@login_requerido
def agregar_resena(id_producto):
    calificacion = int(request.form.get('calificacion'))
    comentario = request.form.get('comentario')
    
    # Verificar que el usuario compró el producto
    ordenes_usuario = Orden.query.filter_by(id_comprador=session['id_usuario']).all()
    ha_comprado = False
    for orden in ordenes_usuario:
        if any(item.id_producto == id_producto for item in orden.items):
            ha_comprado = True
            break
    
    if not ha_comprado:
        flash('Solo puedes calificar productos que hayas comprado', 'danger')
        return redirect(url_for('detalle_producto', id_producto=id_producto))
    
    # Verificar que no haya calificado antes
    resena_existente = Resena.query.filter_by(id_usuario=session['id_usuario'], id_producto=id_producto).first()
    if resena_existente:
        flash('Ya has calificado este producto', 'warning')
        return redirect(url_for('detalle_producto', id_producto=id_producto))
    
    resena = Resena(id_usuario=session['id_usuario'], id_producto=id_producto, calificacion=calificacion, comentario=comentario)
    db.session.add(resena)
    db.session.commit()
    
    flash('¡Reseña agregada exitosamente!', 'success')
    return redirect(url_for('detalle_producto', id_producto=id_producto))

# ============== RUTAS DE ADMINISTRADOR ==============

@app.route('/admin/panel')
@rol_requerido(['Admin'])
def panel_admin():
    total_usuarios = Usuario.query.count()
    total_productos = Producto.query.count()
    total_ordenes = Orden.query.count()
    ingresos_totales = db.session.query(db.func.sum(Orden.total)).scalar() or 0
    
    productos_pendientes = Producto.query.filter_by(esta_aprobado=False).all()
    ordenes_recientes = Orden.query.order_by(Orden.fecha_creacion.desc()).limit(10).all()
    
    return render_template('panel_admin.html', 
                          total_usuarios=total_usuarios,
                          total_productos=total_productos,
                          total_ordenes=total_ordenes,
                          ingresos_totales=ingresos_totales,
                          productos_pendientes=productos_pendientes,
                          ordenes_recientes=ordenes_recientes)

@app.route('/admin/usuarios')
@rol_requerido(['Admin'])
def admin_usuarios():
    usuarios = Usuario.query.all()
    return render_template('admin_usuarios.html', usuarios=usuarios)

@app.route('/admin/crear-admin', methods=['GET', 'POST'])
@login_requerido
def crear_admin():
    # Solo "Nate" puede crear administradores
    if session.get('nombre_usuario') != 'Nate':
        flash('Solo Nate puede crear administradores', 'danger')
        return redirect(url_for('panel_admin'))
    
    if request.method == 'POST':
        nombre_usuario = request.form.get('nombre_usuario')
        email = request.form.get('email')
        contrasena = request.form.get('contrasena')
        
        if Usuario.query.filter_by(nombre_usuario=nombre_usuario).first():
            flash('El usuario ya existe', 'danger')
            return redirect(url_for('crear_admin'))
        
        valido, mensaje = validar_contrasena(contrasena)
        if not valido:
            flash(mensaje, 'danger')
            return redirect(url_for('crear_admin'))
        
        usuario = Usuario(nombre_usuario=nombre_usuario, email=email, rol='Admin')
        usuario.establecer_contrasena(contrasena)
        db.session.add(usuario)
        db.session.commit()
        
        flash(f'Administrador {nombre_usuario} creado exitosamente', 'success')
        return redirect(url_for('admin_usuarios'))
    
    return render_template('crear_admin.html')

@app.route('/admin/eliminar-usuario/<int:id_usuario>', methods=['POST'])
@rol_requerido(['Admin'])
def eliminar_usuario(id_usuario):
    usuario = Usuario.query.get_or_404(id_usuario)
    
    # No permitir eliminar a Nate
    if usuario.nombre_usuario == 'Nate':
        flash('No se puede eliminar al super administrador Nate', 'danger')
        return redirect(url_for('admin_usuarios'))
    
    db.session.delete(usuario)
    db.session.commit()
    flash(f'Usuario {usuario.nombre_usuario} eliminado', 'success')
    return redirect(url_for('admin_usuarios'))

@app.route('/admin/aprobar-producto/<int:id_producto>', methods=['POST'])
@rol_requerido(['Admin'])
def aprobar_producto(id_producto):
    producto = Producto.query.get_or_404(id_producto)
    producto.esta_aprobado = True
    db.session.commit()
    flash(f'Producto "{producto.nombre}" aprobado', 'success')
    return redirect(url_for('panel_admin'))

# ============== RUTAS DE VENDEDOR ==============

@app.route('/vendedor/panel')
@rol_requerido(['Vendedor'])
def panel_vendedor():
    productos = Producto.query.filter_by(id_vendedor=session['id_usuario']).all()
    
    # Calcular ventas del vendedor
    total_ventas = 0
    ingresos_totales = 0
    for producto in productos:
        items_orden = ItemOrden.query.filter_by(id_producto=producto.id).all()
        for item in items_orden:
            total_ventas += item.cantidad
            ingresos_totales += item.precio * item.cantidad
    
    return render_template('panel_vendedor.html', 
                          productos=productos,
                          total_ventas=total_ventas,
                          ingresos_totales=ingresos_totales)

@app.route('/vendedor/agregar-producto', methods=['GET', 'POST'])
@rol_requerido(['Vendedor'])
def agregar_producto():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        precio = float(request.form.get('precio'))
        stock = int(request.form.get('stock'))
        
        if precio <= 0:
            flash('El precio debe ser mayor a 0', 'danger')
            return redirect(url_for('agregar_producto'))
        
        # Manejar imagen
        nombre_imagen = 'producto_default.jpg'
        if 'imagen' in request.files:
            archivo = request.files['imagen']
            if archivo and archivo_permitido(archivo.filename):
                nombre_archivo = secure_filename(archivo.filename)
                ruta_archivo = os.path.join(app.config['UPLOAD_FOLDER'], nombre_archivo)
                archivo.save(ruta_archivo)
                nombre_imagen = nombre_archivo
        
        producto = Producto(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            stock=stock,
            imagen=nombre_imagen,
            id_vendedor=session['id_usuario'],
            esta_aprobado=False
        )
        
        db.session.add(producto)
        db.session.commit()
        
        flash('Producto agregado. Pendiente de aprobación por administrador', 'success')
        return redirect(url_for('panel_vendedor'))
    
    return render_template('agregar_producto.html')

@app.route('/vendedor/editar-producto/<int:id_producto>', methods=['GET', 'POST'])
@rol_requerido(['Vendedor'])
def editar_producto(id_producto):
    producto = Producto.query.get_or_404(id_producto)
    
    if producto.id_vendedor != session['id_usuario']:
        flash('No puedes editar productos de otros vendedores', 'danger')
        return redirect(url_for('panel_vendedor'))
    
    if request.method == 'POST':
        producto.nombre = request.form.get('nombre')
        producto.descripcion = request.form.get('descripcion')
        producto.precio = float(request.form.get('precio'))
        producto.stock = int(request.form.get('stock'))
        
        if producto.precio <= 0:
            flash('El precio debe ser mayor a 0', 'danger')
            return render_template('editar_producto.html', producto=producto)
        
        if 'imagen' in request.files:
            archivo = request.files['imagen']
            if archivo and archivo_permitido(archivo.filename):
                nombre_archivo = secure_filename(archivo.filename)
                ruta_archivo = os.path.join(app.config['UPLOAD_FOLDER'], nombre_archivo)
                archivo.save(ruta_archivo)
                producto.imagen = nombre_archivo
        
        db.session.commit()
        flash('Producto actualizado exitosamente', 'success')
        return redirect(url_for('panel_vendedor'))
    
    return render_template('editar_producto.html', producto=producto)

@app.route('/vendedor/eliminar-producto/<int:id_producto>', methods=['POST'])
@rol_requerido(['Vendedor'])
def eliminar_producto(id_producto):
    producto = Producto.query.get_or_404(id_producto)
    
    if producto.id_vendedor != session['id_usuario']:
        flash('No puedes eliminar productos de otros vendedores', 'danger')
        return redirect(url_for('panel_vendedor'))
    
    db.session.delete(producto)
    db.session.commit()
    flash('Producto eliminado exitosamente', 'success')
    return redirect(url_for('panel_vendedor'))

# ============== RUTAS DE COMPRADOR ==============

@app.route('/carrito')
@rol_requerido(['Comprador'])
def carrito():
    items_carrito = session.get('carrito', {})
    productos = []
    total = 0
    
    for id_producto, cantidad in items_carrito.items():
        producto = Producto.query.get(int(id_producto))
        if producto:
            productos.append({'producto': producto, 'cantidad': cantidad})
            total += producto.precio * cantidad
    
    return render_template('carrito.html', productos=productos, total=total)

@app.route('/agregar-al-carrito/<int:id_producto>', methods=['POST'])
@login_requerido
def agregar_al_carrito(id_producto):
    if session.get('rol') != 'Comprador':
        flash('Solo los compradores pueden agregar al carrito', 'warning')
        return redirect(url_for('detalle_producto', id_producto=id_producto))
    
    cantidad = int(request.form.get('cantidad', 1))
    
    carrito = session.get('carrito', {})
    carrito[str(id_producto)] = carrito.get(str(id_producto), 0) + cantidad
    session['carrito'] = carrito
    
    flash('Producto agregado al carrito', 'success')
    return redirect(url_for('carrito'))

@app.route('/eliminar-del-carrito/<int:id_producto>', methods=['POST'])
@login_requerido
def eliminar_del_carrito(id_producto):
    carrito = session.get('carrito', {})
    if str(id_producto) in carrito:
        del carrito[str(id_producto)]
        session['carrito'] = carrito
        flash('Producto eliminado del carrito', 'info')
    
    return redirect(url_for('carrito'))

@app.route('/checkout', methods=['GET', 'POST'])
@rol_requerido(['Comprador'])
def checkout():
    items_carrito = session.get('carrito', {})
    if not items_carrito:
        flash('El carrito está vacío', 'warning')
        return redirect(url_for('carrito'))
    
    direcciones = Direccion.query.filter_by(id_usuario=session['id_usuario']).all()
    metodos_pago = MetodoPago.query.filter_by(id_usuario=session['id_usuario']).all()
    
    if request.method == 'POST':
        id_direccion = request.form.get('id_direccion')
        id_pago = request.form.get('id_pago')
        
        total = 0
        items_orden = []
        
        for id_producto, cantidad in items_carrito.items():
            producto = Producto.query.get(int(id_producto))
            if producto and producto.stock >= cantidad:
                total += producto.precio * cantidad
                items_orden.append({
                    'id_producto': producto.id,
                    'cantidad': cantidad,
                    'precio': producto.precio
                })
                producto.stock -= cantidad
            else:
                flash(f'Stock insuficiente para {producto.nombre}', 'danger')
                return redirect(url_for('carrito'))
        
        orden = Orden(
            id_comprador=session['id_usuario'],
            total=total,
            id_direccion_envio=id_direccion,
            id_metodo_pago=id_pago,
            estado='Completada'
        )
        
        db.session.add(orden)
        db.session.flush()
        
        for item in items_orden:
            item_orden = ItemOrden(
                id_orden=orden.id,
                id_producto=item['id_producto'],
                cantidad=item['cantidad'],
                precio=item['precio']
            )
            db.session.add(item_orden)
        
        db.session.commit()
        session['carrito'] = {}
        
        flash('¡Compra realizada exitosamente!', 'success')
        return redirect(url_for('historial_ordenes'))
    
    return render_template('checkout.html', direcciones=direcciones, metodos_pago=metodos_pago)

@app.route('/agregar-direccion', methods=['GET', 'POST'])
@rol_requerido(['Comprador'])
def agregar_direccion():
    direcciones_usuario = Direccion.query.filter_by(id_usuario=session['id_usuario']).count()
    
    if direcciones_usuario >= 2:
        flash('Solo puedes tener hasta 2 direcciones guardadas', 'warning')
        return redirect(url_for('perfil'))
    
    if request.method == 'POST':
        direccion = Direccion(
            id_usuario=session['id_usuario'],
            calle=request.form.get('calle'),
            ciudad=request.form.get('ciudad'),
            estado=request.form.get('estado'),
            codigo_postal=request.form.get('codigo_postal'),
            pais=request.form.get('pais'),
            es_predeterminada=request.form.get('es_predeterminada') == 'on'
        )
        
        db.session.add(direccion)
        db.session.commit()
        
        flash('Dirección agregada exitosamente', 'success')
        return redirect(url_for('perfil'))
    
    return render_template('agregar_direccion.html')

@app.route('/agregar-metodo-pago', methods=['GET', 'POST'])
@rol_requerido(['Comprador'])
def agregar_metodo_pago():
    if request.method == 'POST':
        numero_tarjeta = request.form.get('numero_tarjeta')
        titular_tarjeta = request.form.get('titular_tarjeta')
        mes_vencimiento = request.form.get('mes_vencimiento')
        anio_vencimiento = request.form.get('anio_vencimiento')
        cvv = request.form.get('cvv')
        
        # Validar CVV
        if not validar_cvv(cvv):
            flash('CVV inválido (debe tener 3 dígitos)', 'danger')
            return render_template('agregar_metodo_pago.html')
        
        # Validar fecha de vencimiento
        valido, mensaje = validar_vencimiento_tarjeta(mes_vencimiento, anio_vencimiento)
        if not valido:
            flash(mensaje, 'danger')
            return render_template('agregar_metodo_pago.html')
        
        metodo_pago = MetodoPago(
            id_usuario=session['id_usuario'],
            ultimos4_tarjeta=numero_tarjeta[-4:],
            titular_tarjeta=titular_tarjeta,
            mes_vencimiento=int(mes_vencimiento),
            anio_vencimiento=int(anio_vencimiento),
            es_predeterminado=request.form.get('es_predeterminado') == 'on'
        )
        
        db.session.add(metodo_pago)
        db.session.commit()
        
        flash('Método de pago agregado exitosamente', 'success')
        return redirect(url_for('perfil'))
    
    return render_template('agregar_metodo_pago.html')

@app.route('/historial-ordenes')
@login_requerido
def historial_ordenes():
    ordenes = Orden.query.filter_by(id_comprador=session['id_usuario']).order_by(Orden.fecha_creacion.desc()).all()
    return render_template('historial_ordenes.html', ordenes=ordenes)

# ============== PERFIL ==============

@app.route('/perfil', methods=['GET', 'POST'])
@login_requerido
def perfil():
    usuario = Usuario.query.get(session['id_usuario'])
    direcciones = Direccion.query.filter_by(id_usuario=session['id_usuario']).all()
    metodos_pago = MetodoPago.query.filter_by(id_usuario=session['id_usuario']).all()
    
    if request.method == 'POST':
        if 'foto_perfil' in request.files:
            archivo = request.files['foto_perfil']
            if archivo and archivo_permitido(archivo.filename):
                nombre_archivo = secure_filename(archivo.filename)
                ruta_archivo = os.path.join(app.config['UPLOAD_FOLDER'], nombre_archivo)
                archivo.save(ruta_archivo)
                usuario.foto_perfil = nombre_archivo
        
        usuario.nombre_usuario = request.form.get('nombre_usuario', usuario.nombre_usuario)
        db.session.commit()
        
        flash('Perfil actualizado exitosamente', 'success')
        return redirect(url_for('perfil'))
    
    return render_template('perfil.html', usuario=usuario, direcciones=direcciones, metodos_pago=metodos_pago)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Crear carpeta de uploads si no existe
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
    
    app.run(debug=True)