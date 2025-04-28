from django.db import models

class Nivel(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    dificultad = models.IntegerField()

    def __str__(self):
        return self.nombre

class Juego(models.Model):
    titulo = models.CharField(max_length=100)
    nivel = models.ForeignKey(Nivel, on_delete=models.CASCADE)
    instrucciones = models.TextField()

    def __str__(self):
        return self.titulo
