# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Capitulos(models.Model):
    id_cap = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    icono = models.CharField(max_length=100, blank=True, null=True)
    orden = models.IntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'capitulos'


class CasosPrueba(models.Model):
    id_test = models.AutoField(primary_key=True)
    id_lvl = models.ForeignKey('NivelesEjercicios', models.DO_NOTHING, db_column='id_lvl', blank=True, null=True)
    input = models.TextField(blank=True, null=True)
    output = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'casos_prueba'


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Items(models.Model):
    id_item = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    imagen = models.CharField(max_length=100, blank=True, null=True)
    max_usos = models.IntegerField(blank=True, null=True)
    id_personaje = models.ForeignKey('Personajes', models.DO_NOTHING, db_column='id_personaje', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'items'


class MochilaIt(models.Model):
    id_mi = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='id_usuario', blank=True, null=True)
    id_item = models.ForeignKey(Items, models.DO_NOTHING, db_column='id_item', blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mochila_it'


class MochilaPer(models.Model):
    id_mp = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='id_usuario', blank=True, null=True)
    id_personaje = models.ForeignKey('Personajes', models.DO_NOTHING, db_column='id_personaje', blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mochila_per'


class Niveles(models.Model):
    id_nivel = models.AutoField(primary_key=True)
    id_cap = models.ForeignKey(Capitulos, models.DO_NOTHING, db_column='id_cap', blank=True, null=True)
    tipo = models.TextField(blank=True, null=True)  # This field type is a guess.
    titulo = models.CharField(max_length=100, blank=True, null=True)
    puntos_recompensa = models.IntegerField(blank=True, null=True)
    orden = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'niveles'


class NivelesCompletados(models.Model):
    id_completado = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='id_usuario')
    id_nivel = models.ForeignKey(Niveles, models.DO_NOTHING, db_column='id_nivel')
    completado = models.BooleanField()
    puntos_obtenidos = models.IntegerField()
    intentos = models.IntegerField(blank=True, null=True)
    fecha_completado = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'niveles_completados'
        unique_together = (('id_usuario', 'id_nivel'),)


class NivelesEjercicios(models.Model):
    id_lve = models.OneToOneField(Niveles, models.DO_NOTHING, db_column='id_lve', primary_key=True)
    enunciado = models.TextField()
    solucion = models.TextField()

    class Meta:
        managed = False
        db_table = 'niveles_ejercicios'


class NivelesTeoria(models.Model):
    id_lvt = models.OneToOneField(Niveles, models.DO_NOTHING, db_column='id_lvt', primary_key=True)
    contenido = models.TextField()

    class Meta:
        managed = False
        db_table = 'niveles_teoria'


class Personajes(models.Model):
    id_npc = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    imagen = models.CharField(max_length=100, blank=True, null=True)
    id_lvt_unlock = models.ForeignKey(NivelesTeoria, models.DO_NOTHING, db_column='id_lvt_unlock', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'personajes'


class Progreso(models.Model):
    id_progreso = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='id_usuario', blank=True, null=True)
    cap_act = models.ForeignKey(Capitulos, models.DO_NOTHING, db_column='cap_act', blank=True, null=True)
    lvl_act = models.ForeignKey(Niveles, models.DO_NOTHING, db_column='lvl_act', blank=True, null=True)
    exp_total = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'progreso'


class UsoItem(models.Model):
    id_uso = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='id_usuario', blank=True, null=True)
    id_items = models.ForeignKey(Items, models.DO_NOTHING, db_column='id_items', blank=True, null=True)
    id_capi = models.ForeignKey(Capitulos, models.DO_NOTHING, db_column='id_capi', blank=True, null=True)
    id_lvl = models.ForeignKey(Niveles, models.DO_NOTHING, db_column='id_lvl', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'uso_item'


class Usuarios(models.Model):
    id_user = models.AutoField(primary_key=True)
    nombre = models.TextField(blank=True, null=True)  # This field type is a guess.
    username = models.CharField(unique=True, max_length=50, blank=True, null=True)
    contraseña = models.CharField(max_length=100, blank=True, null=True)
    correo = models.CharField(unique=True, max_length=100, blank=True, null=True)
    nivel_usuario = models.TextField(blank=True, null=True)  # This field type is a guess.
    imagen = models.CharField(max_length=100, blank=True, null=True)
    fecha_registro = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuarios'
