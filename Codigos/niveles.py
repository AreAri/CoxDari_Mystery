from modelos.enum import TipoNivel

class Nivel:
    def __init__(self, id_nivel: int, id_cap: int, tipo: TipoNivel, titulo: str, puntos_recompensa: int, orden: int):
        self.id_nivel = id_nivel
        self.id_cap = id_cap
        self.tipo = tipo
        self.titulo = titulo
        self.puntos_recompensa = puntos_recompensa
        self.orden = orden