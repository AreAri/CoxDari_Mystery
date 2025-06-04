from django.db import models

# Tipos personalizados de PostgreSQL (representados como campos planos en Django)

class Usuarios(models.Model):
    id_user = models.AutoField(primary_key=True)
    nombre_nombre = models.CharField(max_length=50)
    nombre_ap_paterno = models.CharField(max_length=50)
    nombre_ap_materno = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    contraseña = models.CharField(max_length=100)
    correo = models.CharField(max_length=100, unique=True)
    nivel_usuario = models.CharField(max_length=20)  # Enum: Novato, Junior, etc.
    imagen = models.CharField(max_length=100, blank=True, null=True)
    fecha_registro = models.DateField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'usuarios'

class Capitulos(models.Model):
    id_cap = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    icono = models.CharField(max_length=100, blank=True, null=True)
    orden = models.IntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'Capitulos'

class Niveles(models.Model):
    id_nivel = models.AutoField(primary_key=True)
    id_cap = models.ForeignKey(Capitulos, on_delete=models.DO_NOTHING, db_column='id_cap')
    tipo = models.CharField(max_length=20)  # Enum: Teoria, Ejercicio, Desafio
    titulo = models.CharField(max_length=100)
    puntos_recompensa = models.IntegerField()
    orden = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'Niveles'

class NivelesTeoria(models.Model):
    id_lvT = models.OneToOneField(Niveles, primary_key=True, on_delete=models.DO_NOTHING, db_column='id_lvT')
    contenido = models.TextField()

    class Meta:
        managed = False
        db_table = 'Niveles_Teoria'

class NivelesEjercicios(models.Model):
    id_lvE = models.OneToOneField(Niveles, primary_key=True, on_delete=models.DO_NOTHING, db_column='id_lvE')
    enunciado = models.TextField()
    solucion = models.TextField()

    class Meta:
        managed = False
        db_table = 'Niveles_Ejercicios'

class CasosPrueba(models.Model):
    id_test = models.AutoField(primary_key=True)
    id_lvl = models.ForeignKey(NivelesEjercicios, on_delete=models.DO_NOTHING, db_column='id_lvl')
    input = models.TextField()
    output = models.TextField()

    class Meta:
        managed = False
        db_table = 'Casos_Prueba'

class Personajes(models.Model):
    id_npc = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    imagen = models.CharField(max_length=100, blank=True, null=True)
    id_lvT_unlock = models.ForeignKey(NivelesTeoria, on_delete=models.DO_NOTHING, db_column='id_lvT_unlock')

    class Meta:
        managed = False
        db_table = 'Personajes'

class Items(models.Model):
    id_item = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    imagen = models.CharField(max_length=100, blank=True, null=True)
    max_usos = models.IntegerField()
    id_personaje = models.ForeignKey(Personajes, on_delete=models.DO_NOTHING, db_column='id_personaje')

    class Meta:
        managed = False
        db_table = 'Items'

class UsoItem(models.Model):
    id_uso = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuarios, on_delete=models.DO_NOTHING, db_column='id_usuario')
    id_items = models.ForeignKey(Items, on_delete=models.DO_NOTHING, db_column='id_items')
    id_capi = models.ForeignKey(Capitulos, on_delete=models.DO_NOTHING, db_column='id_capi')
    id_lvl = models.ForeignKey(Niveles, on_delete=models.DO_NOTHING, db_column='id_lvl')

    class Meta:
        managed = False
        db_table = 'Uso_item'

class MochilaPer(models.Model):
    id_MP = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuarios, on_delete=models.DO_NOTHING, db_column='id_usuario')
    id_personaje = models.ForeignKey(Personajes, on_delete=models.DO_NOTHING, db_column='id_personaje')
    fecha = models.DateField()

    class Meta:
        managed = False
        db_table = 'Mochila_per'

class MochilaIt(models.Model):
    id_MI = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuarios, on_delete=models.DO_NOTHING, db_column='id_usuario')
    id_item = models.ForeignKey(Items, on_delete=models.DO_NOTHING, db_column='id_item')
    fecha = models.DateField()

    class Meta:
        managed = False
        db_table = 'Mochila_It'

class Progreso(models.Model):
    id_progreso = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuarios, on_delete=models.DO_NOTHING, db_column='id_usuario')
    cap_act = models.ForeignKey(Capitulos, on_delete=models.DO_NOTHING, db_column='cap_act')
    lvl_act = models.ForeignKey(Niveles, on_delete=models.DO_NOTHING, db_column='lvl_act')
    exp_total = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'Progreso'

class NivelesCompletados(models.Model):
    id_completado = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuarios, on_delete=models.DO_NOTHING, db_column='id_usuario')
    id_nivel = models.ForeignKey(Niveles, on_delete=models.DO_NOTHING, db_column='id_nivel')
    completado = models.BooleanField(default=True)
    puntos_obtenidos = models.IntegerField()
    intentos = models.IntegerField(default=1)
    fecha_completado = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'Niveles_Completados'
        unique_together = (('id_usuario', 'id_nivel'),)