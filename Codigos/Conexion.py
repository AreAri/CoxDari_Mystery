import psycopg2
from psycopg2 import OperationalError

def conectarBD():
    try: #si te das cuenta no cambia mucho a como lo haces en java
        # Configuracion en base a los parametros dentro de nuestra bd
        conexion = psycopg2.connect(
            host="localhost",      
            database="CoxDari_Mystery",  # Nombre de la base de datos
            user="postgres",    
            password="1316",   # Contraseña (la debes cambiar si la tuya es diferente)
            port="5432"        
        )
#a excepcion de estos 3
        cursor = conexion.cursor() 
        cursor.execute("SELECT 1")  #vereficamos si se conecta 
        resultado = cursor.fetchone()

        if resultado[0] == 1:
            print("Conexión exitosa, bienvenido a la BD")
        else:
            print("Hay un error en la conexion, verifica tus datos")

        cursor.close()
        conexion.close()

    except OperationalError as e:
        print(f"Error de conexión: {e}")

#ejecutamos
conectarBD()