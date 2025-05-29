import xml.etree.ElementTree as ET
from django.http import JsonResponse
from .modelos import Nivel, NivelBloque 

def verificar_bloque(request, nivel_id):
    if request.method == 'POST':
        bloque_xml = request.POST.get('bloque_xml', '')
        
        try:
            nivel = Nivel.objects.get(id=nivel_id)
            bloque = nivel.bloque
            
            # Comparar estructuras XML
            es_correcto = comparar_bloques(bloque_xml, bloque.solucion_xml)
            
            return JsonResponse({
                'correcto': es_correcto,
                'feedback': '¡Solución correcta!' if es_correcto else 'Intenta nuevamente'
            })
            
        except Nivel.DoesNotExist:
            return JsonResponse({'error': 'Nivel no encontrado'}, status=404)
        except AttributeError:
            return JsonResponse({'error': 'Este nivel no es de bloques'}, status=400)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def comparar_bloques(usuario_xml, solucion_xml):
    """Compara dos estructuras de bloques XML"""
    try:
        # Parsear XML
        usuario_root = ET.fromstring(usuario_xml)
        solucion_root = ET.fromstring(solucion_xml)
        
        # Normalizar y comparar
        return normalizar_xml(usuario_root) == normalizar_xml(solucion_root)
    
    except ET.ParseError:
        return False

def normalizar_xml(root):
    """Normaliza la estructura XML para comparación"""
    # Eliminar atributos irrelevantes (posición, id, etc.)
    for elem in root.iter():
        if 'id' in elem.attrib:
            del elem.attrib['id']
        if 'x' in elem.attrib:
            del elem.attrib['x']
        if 'y' in elem.attrib:
            del elem.attrib['y']
    
    # Ordenar elementos hijos para comparación independiente del orden
    for elem in root.iter():
        elem[:] = sorted(elem, key=lambda child: (child.tag, str(child.attrib)))
    
    # Convertir a string normalizado
    return ET.tostring(root, encoding='unicode')