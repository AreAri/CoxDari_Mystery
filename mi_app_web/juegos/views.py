import psycopg2
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.db import connection
from .models import Usuarios, Progreso, NivelesCompletados, Capitulos, Niveles,MochilaIt, MochilaPer
import datetime
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from collections import defaultdict

#----------------------------------------------------------
def index(request):
    return render(request, 'juegos/index.html')

#---------------------------------------------------------
def login_view(request):
    if request.method == 'POST':
        correo = request.POST.get('email')
        password = request.POST.get('password')

        try:
            conn = psycopg2.connect(
                dbname='CoxDari_Mistery',
                user='postgres',
                password='123456789',
                host='localhost',
                port='5432'
            )
            cursor = conn.cursor()
            # Solo buscamos el usuario por correo
            cursor.execute("""
                SELECT id_user,
                       (nombre).nombre || ' ' || (nombre).ap_paterno || ' ' || (nombre).ap_materno AS nombre_completo,
                       contraseña
                FROM Usuarios
                WHERE correo = %s
            """, [correo])
            user = cursor.fetchone()
            cursor.close()
            conn.close()

        except Exception as e:
            return render(request, 'juegos/login.html', {'error': 'Error de conexión con la base de datos.'})

        if user:
            user_id = user[0]
            user_nombre = user[1]
            password_hash = user[2]

            if check_password(password, password_hash):
                request.session['usuario_id'] = user_id
                request.session['usuario_nombre'] = user_nombre
                return redirect('menu')
            else:
                return render(request, 'juegos/login.html', {'error': 'Correo o contraseña incorrectos'})

        else:
            return render(request, 'juegos/login.html', {'error': 'Correo o contraseña incorrectos'})

    return render(request, 'juegos/login.html')

#---------------------------------------------------------

#---------------------------------------------------------
def logout_view(request):
    request.session.flush()
    return redirect('login')

#---------------------------------------------------------
def continuar_nivel(request):
    if 'usuario_id' not in request.session:
        return redirect('login')

    user_id = request.session['usuario_id']

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT lvl_act FROM Progreso WHERE id_usuario = %s
        """, [user_id])
        id_nivel = cursor.fetchone()[0]

    return redirect(f'/nivel/{id_nivel}/')  # Esta URL la crearemos luego

#---------------------------------------------------------
def jugar_nivel(request):
    if 'usuario_id' not in request.session:
        return redirect('login')

    id_usuario = request.session['usuario_id']

    with connection.cursor() as cursor:
        # Obtener progreso actual
        cursor.execute("""
            SELECT N.id_nivel, N.tipo, N.titulo, NT.contenido, NE.enunciado
            FROM Progreso P
            JOIN Niveles N ON P.lvl_act = N.id_nivel
            LEFT JOIN Niveles_Teoria NT ON NT.id_lvT = N.id_nivel
            LEFT JOIN Niveles_Ejercicios NE ON NE.id_lvE = N.id_nivel
            WHERE P.id_usuario = %s
        """, [id_usuario])
        nivel = cursor.fetchone()

    if not nivel:
        return render(request, 'jugar_nivel.html', {'mensaje': 'No hay nivel disponible'})

    id_nivel, tipo, titulo, contenido, enunciado = nivel

    # Si POST, validar respuesta (solo para ejercicio)
    if request.method == 'POST' and tipo == 'Ejercicio':
        respuesta = request.POST.get('respuesta', '').strip()

        with connection.cursor() as cursor:
            cursor.execute("SELECT solucion FROM Niveles_Ejercicios WHERE id_lvE = %s", [id_nivel])
            solucion = cursor.fetchone()[0].strip()

            if respuesta.lower() == solucion.lower():
                # Insertar en Niveles_Completados → triggers hacen el resto
                cursor.execute("""
                    INSERT INTO Niveles_Completados (id_usuario, id_nivel, puntos_obtenidos)
                    VALUES (%s, %s, (SELECT puntos_recompensa FROM Niveles WHERE id_nivel = %s))
                    ON CONFLICT (id_usuario, id_nivel) DO NOTHING
                """, [id_usuario, id_nivel, id_nivel])

                return redirect('menu')  # éxito → vuelve al menú
            else:
                mensaje = "Respuesta incorrecta. Intenta nuevamente."
                return render(request, 'jugar_nivel.html', {
                    'tipo': tipo, 'titulo': titulo, 'enunciado': enunciado,
                    'mensaje': mensaje
                })

    # Mostrar teoría o ejercicio
    return render(request, 'jugar_nivel.html', {
        'tipo': tipo,
        'titulo': titulo,
        'contenido': contenido,
        'enunciado': enunciado,
    })

#---------------------------------------------------------
def dictfetchall(cursor):
    """Convierte los resultados del cursor a una lista de diccionarios."""
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
#------------------------------------------------------
def mochila(request):

    if 'usuario_id' not in request.session:
        return redirect('login')

    user_id = request.session['usuario_id']

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT mi.id_MI, mi.fecha, i.nombre, i.descripcion
            FROM mochila_it mi
            JOIN items i ON mi.id_item = i.id_item
            WHERE mi.id_usuario = %s
        """, [request.session.get("usuario_id")])
        mochila_items = dictfetchall(cursor)
    
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT username, correo,
                   (nombre).nombre, (nombre).ap_paterno, (nombre).ap_materno,
                   contraseña,imagen
            FROM Usuarios
            WHERE id_user = %s
        """, [user_id])
        row = cursor.fetchone()

    if not row:
        messages.error(request, "Usuario no encontrado.")
        return redirect('login')

    usuario_menu = {
        'username': row[0],
        'correo': row[1],
        'nombre': row[2],
        'ap_paterno': row[3],
        'ap_materno': row[4],
        'contraseña': '',  # Aquí mostrarás la contraseña hasheada, no la real
        'imagen':row[6]
    }

    # También pasar datos para menú (opcional)
    contexto_menu = {
        'username': usuario_menu['username'],
        'imagen_url':usuario_menu['imagen'],  # O obtén URL si tienes campo imagen
        'rango': '',         # Agrega rango si lo tienes
        'exp': 0,            # Agrega experiencia si aplica
        'capitulo': '',      # Agrega capítulo actual si aplica
        'nivel': '',         # Agrega nivel actual si aplica
        'datos_usuario': usuario_menu,
    }


    return render(request, 'juegos/mochila.html', {
        'items': mochila_items,
        'username': usuario_menu['username'],
        'imagen_url': usuario_menu['imagen'],
    })
#---------------------------------------------------------
def registro(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        ap_paterno = request.POST.get('ap_paterno')
        ap_materno = request.POST.get('ap_materno')
        username = request.POST.get('username')
        correo = request.POST.get('correo')
        contraseña = request.POST.get('contraseña')
        imagen = request.POST.get('imagen') or 'default.png'

        try:
            conn = psycopg2.connect(
                dbname='CoxDari_Mistery',
                user='postgres',
                password='123456789',
                host='localhost',
                port='5432'
            )
            cursor = conn.cursor()
            # Verificar si ya existe un usuario con el mismo username o correo
            cursor.execute("SELECT * FROM Usuarios WHERE username = %s OR correo = %s", (username, correo))
            existing_user = cursor.fetchone()

            if existing_user:
                messages.error(request, "Este usuario o correo ya está registrado.")
                return redirect('registro')

            password_hash = make_password(contraseña)
            cursor.execute("""
                INSERT INTO Usuarios (nombre, username, contraseña, correo, nivel_usuario, imagen, fecha_registro)
                VALUES (ROW(%s, %s, %s), %s, %s, %s, DEFAULT, %s, %s)
            """, (
                nombre, ap_paterno, ap_materno,
                username,
                password_hash,
                correo,
                imagen,
                datetime.date.today()
            ))

            conn.commit()
            cursor.close()
            conn.close()

            messages.success(request, "¡Usuario registrado con éxito! Ahora inicia sesión.")
            return redirect('login')  # Asegúrate que el nombre de tu URL de login sea 'login'

        except Exception as e:
            print(e)
            messages.error(request, "Ocurrió un error al registrar el usuario.")
            return redirect('registro')

    return render(request, 'juegos/registro.html')

#-------------------------------------------------------------------------------
def menu_principal(request):
    id_usuario = request.session.get('usuario_id')
    if not id_usuario:
        return redirect('login')

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id_user,
                (nombre).nombre AS nombre,
                (nombre).ap_paterno AS ap_paterno,
                (nombre).ap_materno AS ap_materno,
                username,
                nivel_usuario,
                imagen
            FROM Usuarios
            WHERE id_user = %s
        """, [id_usuario])
        usuario_raw = cursor.fetchone()

        if not usuario_raw:
            return redirect('login')

        usuario = {
            'id': usuario_raw[0],
            'nombre_completo': f"{usuario_raw[1]} {usuario_raw[2]} {usuario_raw[3]}",
            'username': usuario_raw[4],
            'nivel_usuario': usuario_raw[5],
            'imagen': usuario_raw[6],
        }

        cursor.execute("""
            SELECT p.exp_total, c.nombre, n.titulo
            FROM Progreso p
            JOIN Capitulos c ON p.cap_act = c.id_cap
            JOIN Niveles n ON p.lvl_act = n.id_nivel
            WHERE p.id_usuario = %s
            """, [id_usuario])

        progreso_raw = cursor.fetchone()

        if not progreso_raw:
            return redirect('inicializar_progreso')

        progreso = {
            'exp': progreso_raw[0],
            'capitulo': progreso_raw[1],
            'nivel': progreso_raw[2],
        }

        # Obtener niveles completados
        cursor.execute("""
            SELECT id_nivel FROM Niveles_Completados WHERE id_usuario = %s
        """, [id_usuario])
        niveles_completados = [r[0] for r in cursor.fetchall()]

        # Obtener todos los capítulos y niveles (simplificado)
        cursor.execute("SELECT id_cap, nombre FROM Capitulos ORDER BY orden")
        capitulos = cursor.fetchall()

        cursor.execute("""
            SELECT id_nivel, tipo, titulo, puntos_recompensa, id_cap
            FROM Niveles
            ORDER BY orden
        """)
        niveles = cursor.fetchall()

    # Armar niveles_data
    niveles_data = []
    for id_cap, nombre_cap in capitulos:
        for nivel in niveles:
            if nivel[4] == id_cap:
                niveles_data.append({
                    'capitulo': nombre_cap,
                    'nivel_id': nivel[0],
                    'tipo': nivel[1],
                    'titulo': nivel[2],
                    'puntos': nivel[3],
                    'completado': nivel[0] in niveles_completados,
                    'desbloqueado': False  # si quieres lógica más específica la ajustamos
                })

    contexto = {
        'username': usuario['username'],
        'rango': usuario['nivel_usuario'],
        'exp': progreso['exp'],
        'capitulo': progreso['capitulo'],
        'nivel': progreso['nivel'],
        'niveles_data': niveles_data,
        'imagen_url': usuario['imagen'],  # <-- importante
    }

    return render(request, 'juegos/menu_principal.html', contexto)

#--------------------------------------------------------------------------------

def perfil_usuario(request):
    # Validar sesión
    if 'usuario_id' not in request.session:
        return redirect('login')

    user_id = request.session['usuario_id']

    if request.method == 'POST':
        if 'editar' in request.POST:
            # Obtener datos del formulario
            username = request.POST.get('username').strip()
            correo = request.POST.get('correo').strip()
            nombre = request.POST.get('nombre').strip()
            ap_paterno = request.POST.get('ap_paterno').strip()
            ap_materno = request.POST.get('ap_materno').strip()
            nueva_contraseña = request.POST.get('contraseña').strip()
            imagen = request.POST.get('imagen') or 'default.png'

            # Validar campos (sin requerir contraseña si no se desea cambiar)
            if not all([username, correo, nombre, ap_paterno, ap_materno]):
                messages.error(request, "Los campos no pueden estar vacíos.")
            else:
                try:
                    # Obtener contraseña actual si el campo viene vacío
                    if nueva_contraseña:
                        contraseña_final = make_password(nueva_contraseña)
                    else:
                        with connection.cursor() as cursor:
                            cursor.execute("SELECT contraseña FROM Usuarios WHERE id_user = %s", [user_id])
                            contraseña_final = cursor.fetchone()[0]  # contraseña actual

                    # Actualizar datos
                    with connection.cursor() as cursor:
                        cursor.execute("""
                            UPDATE Usuarios
                            SET username = %s,
                                correo = %s,
                                nombre = ROW(%s, %s, %s),
                                contraseña = %s,
                                imagen = %s
                            WHERE id_user = %s
                        """, [username, correo, nombre, ap_paterno, ap_materno, contraseña_final, imagen, user_id])

                    messages.success(request, "Perfil actualizado correctamente.")
                    request.session['usuario_nombre'] = f"{nombre} {ap_paterno} {ap_materno}"
                except Exception as e:
                    messages.error(request, f"Error al actualizar perfil: {e}")

        elif 'eliminar' in request.POST:
            try:
                with connection.cursor() as cursor:
                    cursor.execute("DELETE FROM Usuarios WHERE id_user = %s", [user_id])
                request.session.flush()  # cerrar sesión
                messages.success(request, "Cuenta eliminada correctamente.")
                return redirect('login')
            except Exception as e:
                messages.error(request, f"Error al eliminar cuenta: {e}")

    # Cargar datos para mostrar en el formulario (GET o POST después)
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT username, correo,
                   (nombre).nombre, (nombre).ap_paterno, (nombre).ap_materno,
                   contraseña,imagen
            FROM Usuarios
            WHERE id_user = %s
        """, [user_id])
        row = cursor.fetchone()

    if not row:
        messages.error(request, "Usuario no encontrado.")
        return redirect('login')

    datos_usuario = {
        'username': row[0],
        'correo': row[1],
        'nombre': row[2],
        'ap_paterno': row[3],
        'ap_materno': row[4],
        'contraseña': '',  # Aquí mostrarás la contraseña hasheada, no la real
        'imagen':row[6]
    }

    # También pasar datos para menú (opcional)
    contexto_menu = {
        'username': datos_usuario['username'],
        'imagen_url':datos_usuario['imagen'],  # O obtén URL si tienes campo imagen
        'rango': '',         # Agrega rango si lo tienes
        'exp': 0,            # Agrega experiencia si aplica
        'capitulo': '',      # Agrega capítulo actual si aplica
        'nivel': '',         # Agrega nivel actual si aplica
        'datos_usuario': datos_usuario,
    }

    return render(request, 'juegos/perfil_usuario.html', contexto_menu)