from enum import Enum

#dado a que tenemos emun es nuestra clase de los enum
class Rango(Enum):
    NOVATO = "Novato"
    JUNIOR = "Junior"
    INTERMEDIO = "Intermedio"
    SEMI_SENIOR = "Semi Senior"
    EXPERTO = "Experto"
    SENIOR = "Senior"

class TipoNivel(Enum):
    TEORIA = "Teoria"
    EJERCICIO = "Ejercicio"
    DESAFIO = "Desafio"

class NombreCompleto:
    def __init__(self, nombre: str, ap_paterno: str, ap_materno: str):
        self.nombre = nombre
        self.ap_paterno = ap_paterno
        self.ap_materno = ap_materno