from django.shortcuts import render, redirect
from .models import Nivel
from django.db import connection

def index(request):
    return render(request, 'juegos/index.html')

def login_view(request):
    if request.method == 'POST':
        correo = request.POST.get('email')
        password = request.POST.get('password')

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id_user,
                       (nombre).nombre || ' ' || (nombre).ap_paterno || ' ' || (nombre).ap_materno AS nombre_completo
                FROM Usuarios
                WHERE correo = %s AND contraseña = %s
            """, [correo, password])
            user = cursor.fetchone()
        if user:
            request.session['usuario_id'] = user[0]
            request.session['usuario_nombre'] = user[1]
            return redirect('menu')  # Ajusta esto al nombre real de tu vista principal
        else:
            return render(request, 'juegos/login.html', {'error': 'Correo o contraseña incorrectos'})

    return render(request, 'juegos/login.html')

def menu_principal(request):
    if 'usuario_id' not in request.session:
        return redirect('login')

    user_id = request.session['usuario_id']

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT u.username, u.nivel_usuario, p.exp_total, c.nombre, n.titulo
            FROM Usuarios u
            JOIN Progreso p ON u.id_user = p.id_usuario
            JOIN Capitulos c ON p.cap_act = c.id_cap
            JOIN Niveles n ON p.lvl_act = n.id_nivel
            WHERE u.id_user = %s
        """, [user_id])
        datos = cursor.fetchone()

    contexto = {
        'username': datos[0],
        'rango': datos[1],
        'exp': datos[2],
        'capitulo': datos[3],
        'nivel': datos[4],
    }

    return render(request, 'juegos/menu_principal.html', contexto)

def logout_view(request):
    request.session.flush()
    return redirect('login')

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