
class Capitulo:
    def __init__(self, id_cap: int, nombre: str, descripcion: str, icono: str, orden: int):
        self.id_cap = id_cap
        self.nombre = nombre
        self.descripcion = descripcion
        self.icono = icono
        self.orden = orden

    def __repr__(self):
        return f"Capitulo(id_cap={self.id_cap}, nombre={self.nombre})"