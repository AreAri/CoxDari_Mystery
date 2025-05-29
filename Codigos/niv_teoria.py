from modelos.enum import TipoNivel
from niveles import Nivel

class NivelTeoria(Nivel):
    def __init__(self, id_nivel: int, id_cap: int, tipo: TipoNivel, titulo: str, puntos_recompensa: int, orden: int, contenido: str):
        super().__init__(id_nivel, id_cap, tipo, titulo, puntos_recompensa, orden)
        self.contenido = contenido