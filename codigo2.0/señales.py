# como tal tenemos trigger pero en esre caso tube problemas al impelmentarlos y surguio esta obcion de tener señales por parte de django
from django.db.models.signals import post_save
from django.dispatch import receiver
from .modelos import User, Progreso, NivelCompletado, Capitulo, Nivel

@receiver(post_save, sender=User)
def crear_progreso_usuario(sender, instance, created, **kwargs):
    if created:
        primer_capitulo = Capitulo.objects.order_by('orden').first()
        primer_nivel = Nivel.objects.order_by('orden').first()
        Progreso.objects.create(
            usuario=instance,
            capitulo_actual=primer_capitulo,
            nivel_actual=primer_nivel
        )

@receiver(post_save, sender=NivelCompletado)
def actualizar_progreso(sender, instance, created, **kwargs):
    if created and instance.completado:
        # Actualizar experiencia
        progreso = Progreso.objects.get(usuario=instance.usuario)
        progreso.exp_total += instance.puntos_obtenidos
        progreso.save()
        
        # Buscar siguiente nivel
        nivel_actual = instance.nivel
        siguiente_nivel = Nivel.objects.filter(
            capitulo=nivel_actual.capitulo,
            orden__gt=nivel_actual.orden
        ).order_by('orden').first()
        
        if siguiente_nivel:
            progreso.nivel_actual = siguiente_nivel
            progreso.save()
        else:
            # Buscar siguiente capítulo
            siguiente_capitulo = Capitulo.objects.filter(
                orden__gt=nivel_actual.capitulo.orden
            ).order_by('orden').first()
            
            if siguiente_capitulo:
                primer_nivel_sig = siguiente_capitulo.niveles.order_by('orden').first()
                progreso.capitulo_actual = siguiente_capitulo
                progreso.nivel_actual = primer_nivel_sig
                progreso.save()

@receiver(post_save, sender=Progreso)
def actualizar_rango_usuario(sender, instance, **kwargs):
    RANGOS = [
        (500, 'Senior'),
        (300, 'Experto'),
        (200, 'Semi Senior'),
        (100, 'Intermedio'),
        (50, 'Junior'),
        (0, 'Novato')
    ]
    
    nuevo_rango = 'Novato'
    for exp, rango in RANGOS:
        if instance.exp_total >= exp:
            nuevo_rango = rango
            break
    
    if instance.usuario.nivel_usuario != nuevo_rango:
        instance.usuario.nivel_usuario = nuevo_rango
        instance.usuario.save()