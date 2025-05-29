from datetime import date
from modelos.enum import Rango
from modelos.enum import NombreCompleto

class Usuario:
    def __init__(self, id_user, nombre: NombreCompleto, username, contraseña, 
                 correo, nivel_usuario=Rango.NOVATO, imagen=None, 
                 fecha_registro=date.today()):
        self.id_user = id_user
        self.nombre = nombre
        self.username = username
        self.contraseña = contraseña
        self.correo = correo
        self.nivel_usuario = nivel_usuario
        self.imagen = imagen
        self.fecha_registro = fecha_registro

    def __repr__(self):
        return f"Usuario(id_user={self.id_user}, username={self.username})"

    def __eq__(self, other):
        return self.id_user == other.id_user

