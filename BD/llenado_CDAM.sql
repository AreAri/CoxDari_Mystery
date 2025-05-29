INSERT INTO Capitulos (nombre, descripcion, icono, orden) VALUES
('Introducción', 'Conceptos básicos de estructuras de datos, lo que esconde la mascara de programación', NULL, 1),
('Apuntadores', 'Todo lo que debes saber del señor Apuntador y sus aliados', NULL, 2),
('Listas Enlazadas', 'Listas simples y doblemente enlazadas... que tan complidado sera?', NULL, 3);


INSERT INTO Niveles (id_cap, tipo, titulo, puntos_recompensa, orden) VALUES
(1, 'Teoria', 'Qué son las ED?', 10, 1),
(1, 'Ejercicio', 'Identificar una ED', 20, 2),
(1, 'Ejercicio', 'Clasifica las ED', 15, 1),
(2, 'Teoria', 'Señor apuntador y sus aliados los formatos', 20, 1),
(2, 'Ejercicio', 'Idetifica los direntes formatos', 15, 2),
(2, 'Ejercicio', 'Creando al señor apuntador', 15, 3);

INSERT INTO Niveles_Teoria (id_lvT, contenido) VALUES
(1, 'Definición y clasificación de estructuras...'),
(4, 'Es algo que apunta a algo o una Variable que apunta a la direccion de otra variables o Una forma de hacer referencia a una variable sin tomarla directamente...');

INSERT INTO Niveles_Ejercicios (id_lvE, enunciado, solucion) VALUES
(2, 'Casifica cuales son las estructuras de datos y cuales no ', 'pilas, colas, listas, arboles, grafos'),
(3, 'Identifica cuales son las ED lineales y las no lineales', 'Lineales: Array, Lista | No Lineales: Árbol, Grafo'),
(5, 'Recuerdas los aliados? veremos si conoces que esonde cada unoa de ellos', '%d -- entero, %f -- flotante, %c -- caracter'),
(6, 'Veremos como crear a nuestros señor apuntador y como llamarlo si lo necesitas', 'dato = &numero dato2 = *dato imprimir dato2'),
(7, 'Mi primer puntero funcional, con lo que tienes como harias un puntero para darle un valor','int main() {int numero = 10; int *puntero; puntero = &numero; 
  printf("Valor de numero: %d\n", numero); printf("Valor usando puntero: %d\n", *puntero); return 0;}';

INSERT INTO Personajes (nombre, descripcion, imagen, id_lvT_unlock) VALUES
('Yuli la gran sabia', 'Tiene una Maestria en Redes, puedes preguntar lo que sea es muy lista',NULL, 1),
('Doc Ceron', 'Experto en redes y C, si necesitas a alguien que resuelva el es tu mejor opcion', null, 4);

INSERT INTO Items (nombre, descripcion, imagen, max_usos, id_personaje) VALUES
('Libro de la sabiduria', 'Aqui se ocultas los mayores secretos dentro de la programacion pero sera revelados solo a los elegidos', null, 2, 1),
('El cafe del poder', 'La vieja confiable cuando de energias se habla', null, 4, 2);
