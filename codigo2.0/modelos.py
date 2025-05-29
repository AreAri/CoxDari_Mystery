#volvio todo a uno solo porque como esta causando probelmas 
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator

class NombreCompleto(models.Model):
    nombre = models.CharField(max_length=50)
    ap_paterno = models.CharField(max_length=50)
    ap_materno = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        abstract = True

class User(AbstractUser, NombreCompleto):
    RANGO_CHOICES = [
        ('Novato', 'Novato'),
        ('Junior', 'Junior'),
        ('Intermedio', 'Intermedio'),
        ('Semi Senior', 'Semi Senior'),
        ('Experto', 'Experto'),
        ('Senior', 'Senior')
    ]
    
    nivel_usuario = models.CharField(
        max_length=20, 
        choices=RANGO_CHOICES, 
        default='Novato'
    )
    imagen = models.ImageField(upload_to='usuarios/', blank=True, null=True)
    fecha_registro = models.DateField(auto_now_add=True)
    
    # Eliminar campos no necesarios de AbstractUser
    first_name = None
    last_name = None

class Capitulo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    icono = models.CharField(max_length=100, blank=True, null=True)
    orden = models.IntegerField(unique=True)

    class Meta:
        ordering = ['orden']
    
    def __str__(self):
        return self.nombre

class Nivel(models.Model):
    TIPO_CHOICES = [
        ('Teoria', 'Teoría'),
        ('Ejercicio', 'Ejercicio'),
        ('Desafio', 'Desafío')
    ]
    
    capitulo = models.ForeignKey(Capitulo, on_delete=models.CASCADE, related_name='niveles')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    titulo = models.CharField(max_length=100)
    puntos_recompensa = models.IntegerField(validators=[MinValueValidator(1)])
    orden = models.IntegerField()

    class Meta:
        ordering = ['orden']
        unique_together = ['capitulo', 'orden']
    
    def __str__(self):
        return f"{self.capitulo.nombre} - {self.titulo}"

class NivelTeoria(models.Model):
    nivel = models.OneToOneField(
        Nivel, 
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='teoria'
    )
    contenido = models.TextField()
    
    def __str__(self):
        return f"Teoría: {self.nivel.titulo}"

class NivelEjercicio(models.Model):
    nivel = models.OneToOneField(Nivel, on_delete=models.CASCADE, related_name='ejercicio')
    enunciado = models.TextField()
    solucion = models.TextField()

class NivelBloque(models.Model):
    nivel = models.OneToOneField(Nivel, on_delete=models.CASCADE, related_name='bloque')
    enunciado = models.TextField()
    # Almacenamos el XML esperado o una representación JSON de la solución
    solucion_xml = models.TextField()

# class CasoPrueba(models.Model):
#     ejercicio = models.ForeignKey(NivelEjercicio, on_delete=models.CASCADE, related_name='casos_prueba')
#     input = models.TextField()
#     output = models.TextField()
    
#     def __str__(self):
#         return f"Caso #{self.id} - {self.ejercicio.nivel.titulo}"

class Personaje(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='personajes/', blank=True, null=True)
    nivel_teoria_unlock = models.ForeignKey(
        NivelTeoria, 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True,
        related_name='personajes_desbloqueados'
    )
    
    def __str__(self):
        return self.nombre

class Item(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='items/', blank=True, null=True)
    max_usos = models.IntegerField(default=1)
    personaje = models.ForeignKey(Personaje, on_delete=models.CASCADE, related_name='items')
    
    def __str__(self):
        return self.nombre

class UsoItem(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    capitulo = models.ForeignKey(Capitulo, on_delete=models.CASCADE)
    nivel = models.ForeignKey(Nivel, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Uso de item"
        verbose_name_plural = "Usos de items"

class MochilaPersonaje(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    personaje = models.ForeignKey(Personaje, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['usuario', 'personaje']
        verbose_name = "Personaje en mochila"
        verbose_name_plural = "Personajes en mochila"

class MochilaItem(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Item en mochila"
        verbose_name_plural = "Items en mochila"

class Progreso(models.Model):
    usuario = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='progreso'
    )
    capitulo_actual = models.ForeignKey(
        Capitulo, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='progreso_actual'
    )
    nivel_actual = models.ForeignKey(
        Nivel, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='progreso_actual'
    )
    exp_total = models.IntegerField(default=0)
    
    def __str__(self):
        return f"Progreso de {self.usuario.username}"

class NivelCompletado(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nivel = models.ForeignKey(Nivel, on_delete=models.CASCADE)
    completado = models.BooleanField(default=True)
    puntos_obtenidos = models.IntegerField()
    intentos = models.IntegerField(default=1)
    fecha_completado = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['usuario', 'nivel']
        verbose_name = "Nivel completado"
        verbose_name_plural = "Niveles completados"
    
    def __str__(self):
        return f"{self.usuario.username} - {self.nivel.titulo}"