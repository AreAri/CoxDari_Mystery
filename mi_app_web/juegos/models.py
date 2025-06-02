from django.db import models
from django.utils import timezone

class Rango(models.TextChoices):
    NOVATO = "Novato"
    JUNIOR = "Junior"
    INTERMEDIO = "Intermedio"
    SEMI_SENIOR = "Semi Senior"
    EXPERTO = "Experto"
    SENIOR = "Senior"

class TipoNivel(models.TextChoices):
    TEORIA = "Teoria"
    EJERCICIO = "Ejercicio"
    DESAFIO = "Desafio"

class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    ap_paterno = models.CharField(max_length=50)
    ap_materno = models.CharField(max_length=50)
    username = models.CharField(max_length=30, unique=True)
    contraseña = models.CharField(max_length=128)
    correo = models.EmailField(unique=True)
    nivel_usuario = models.CharField(max_length=20, choices=Rango.choices, default=Rango.NOVATO)
    imagen = models.ImageField(upload_to='usuarios/', null=True, blank=True)
    fecha_registro = models.DateField(default=timezone.now)

    def __str__(self):
        return self.username

class Capitulo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    icono = models.CharField(max_length=255)
    orden = models.IntegerField(default=0)
    capitulo_anterior = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.nombre

class Nivel(models.Model):
    capitulo = models.ForeignKey(Capitulo, on_delete=models.CASCADE, default=1)
    tipo = models.CharField(max_length=20, choices=TipoNivel.choices,default="")
    titulo = models.CharField(max_length=100,default="")
    puntos_recompensa = models.IntegerField(default=0)
    orden = models.IntegerField(default=1)
    nivel_anterior = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.titulo

class NivelTeoria(models.Model):
    nivel = models.OneToOneField(Nivel, on_delete=models.CASCADE, primary_key=True)
    contenido = models.TextField(default="")

class CasoPrueba(models.Model):
    input = models.TextField(default="")
    output = models.TextField(default="")

class NivelEjercicio(models.Model):
    nivel = models.OneToOneField(Nivel, on_delete=models.CASCADE, primary_key=True)
    enunciado = models.TextField(default="")
    solucion = models.TextField(default="")
    casos_prueba = models.ManyToManyField(CasoPrueba, blank=True)

class Personaje(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(default="")
    imagen = models.CharField(max_length=255)
    nivel_desbloqueo = models.ForeignKey(Nivel, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.nombre

class Item(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(default="")
    imagen = models.CharField(max_length=255)
    max_usos = models.IntegerField(default="")
    personaje = models.ForeignKey(Personaje, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.nombre

class MochilaPersonaje(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    personaje = models.ForeignKey(Personaje, on_delete=models.CASCADE)
    fecha = models.DateField(default=timezone.now)

class MochilaItem(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    fecha = models.DateField(default=timezone.now)

class Progreso(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    capitulo_actual = models.ForeignKey(Capitulo, on_delete=models.SET_NULL, null=True)
    nivel_actual = models.ForeignKey(Nivel, on_delete=models.SET_NULL, null=True)
    exp_total = models.IntegerField(default=0)

class UsoItem(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    capitulo = models.ForeignKey(Capitulo, on_delete=models.CASCADE)
    nivel = models.ForeignKey(Nivel, on_delete=models.CASCADE)

class NivelCompletado(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nivel = models.ForeignKey(Nivel, on_delete=models.CASCADE)
    completado = models.BooleanField(default=True)
    puntos_obtenidos = models.IntegerField(default=0)
    intentos = models.IntegerField(default=1)
    fecha_completado = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('usuario', 'nivel')
