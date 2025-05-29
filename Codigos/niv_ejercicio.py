from modelos.enum import TipoNivel
from modelos.niveles import Nivel

class NivelEjercicio(Nivel):
    def __init__(self, id_nivel: int, id_cap: int, tipo: TipoNivel, titulo: str, puntos_recompensa: int, orden: int, 
                 enunciado: str, solucion: str, casos_prueba: List[CasoPrueba] = None):
        super().__init__(id_nivel, id_cap, tipo, titulo, puntos_recompensa, orden)
        self.enunciado = enunciado
        self.solucion = solucion
        self.casos_prueba = casos_prueba if casos_prueba else []