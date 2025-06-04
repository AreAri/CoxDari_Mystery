import psycopg2
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.db import connection
from .models import Usuarios, Progreso, NivelesCompletados, Capitulos, Niveles
import datetime

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
            cursor.execute("""
                SELECT id_user,
                       (nombre).nombre || ' ' || (nombre).ap_paterno || ' ' || (nombre).ap_materno AS nombre_completo
                FROM Usuarios
                WHERE correo = %s AND contraseña = %s
            """, [correo, password])
            user = cursor.fetchone()
            cursor.close()
            conn.close()
        except Exception as e:
            return render(request, 'juegos/login.html', {'error': 'Error de conexión con la base de datos.'})

        if user:
            request.session['usuario_id'] = user[0]
            request.session['usuario_nombre'] = user[1]
            return redirect('menu')
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
def mochila(request):
    return render(request, 'mochila.html')

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

            cursor.execute("""
                INSERT INTO Usuarios (nombre, username, contraseña, correo, nivel_usuario, imagen, fecha_registro)
                VALUES (ROW(%s, %s, %s), %s, %s, %s, DEFAULT, %s, %s)
            """, (
                nombre, ap_paterno, ap_materno,
                username,
                contraseña,
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
    # Suponiendo que el login ya guardó el ID del usuario en sesión
    id_usuario = request.session.get('id_usuario')
    if not id_usuario:
        return redirect('login')  # O como se llame tu vista de login

    try:
        usuario = Usuarios.objects.get(id_user=id_usuario)
        progreso = Progreso.objects.get(id_usuario=id_usuario)
    except Usuarios.DoesNotExist:
        return redirect('login')
    except Progreso.DoesNotExist:
        # Podrías inicializar progreso si es nuevo
        return redirect('inicializar_progreso')

    niveles_completados = NivelesCompletados.objects.filter(
        id_usuario=id_usuario
    ).values_list('id_nivel', flat=True)

    capitulos = Capitulos.objects.all().order_by('orden')
    niveles = Niveles.objects.all().order_by('orden')

    niveles_data = []
    for cap in capitulos:
        niveles_cap = niveles.filter(id_cap=cap.id_cap)
        for lvl in niveles_cap:
            niveles_data.append({
                'capitulo': cap.nombre,
                'nivel_id': lvl.id_nivel,
                'tipo': lvl.tipo,
                'titulo': lvl.titulo,
                'puntos': lvl.puntos_recompensa,
                'completado': lvl.id_nivel in niveles_completados,
                'desbloqueado': lvl.id_nivel == progreso.lvl_act.id_nivel or lvl.id_nivel in niveles_completados,
            })

    contexto = {
        'username': usuario.username,
        'rango': usuario.nivel_usuario,
        'exp': progreso.exp_total,
        'capitulo': progreso.cap_act.nombre,
        'nivel': progreso.lvl_act.titulo,
        'niveles_data': niveles_data,
    }

    return render(request, 'juegos/menu.html', contexto)
