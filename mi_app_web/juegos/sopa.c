#include <stdio.h>
#include <string.h>
#include <ctype.h>

#define SIZE 10
#define MAX_PALABRAS 35
#define LONGITUD_MAX 20

// Lista oficial de palabras
const char* lista_palabras[MAX_PALABRAS] = {
    "CAERIA", "CAIDOS", "CAQUI", "CARRO", "CONSOLIDAS",
    "AISLANTE", "AJA", "AJO", "AQUILATAR", "UCLES",
    "UNI", "URANO", "USA", "CENA", "CESO",
    "CID", "COPIE", "CROE", "RIAIS", "RILE",
    "ROIA", "LIA", "LOA", "BOCIO", "SINO",
    "DAS", "DESATA", "LELAS", "LIVIANO", "LOS",
    "CACAHUATE", "COENDU", "ACROBACIA", "ARAS", "ASOLAIS"
};

// Arreglo para registrar palabras ya colocadas
int palabras_colocadas[MAX_PALABRAS] = {0};

// Función para inicializar el tablero
void inicializarTablero(char tablero[SIZE][SIZE]) {
    for (int i = 0; i < SIZE; i++)
        for (int j = 0; j < SIZE; j++)
            tablero[i][j] = ' ';
}

// Función para imprimir el tablero
void imprimirTablero(char tablero[SIZE][SIZE]) {
    printf("\n  ");
    for (int j = 0; j < SIZE; j++)
        printf("%d ", j);
    printf("\n");

    for (int i = 0; i < SIZE; i++) {
        printf("%d ", i);
        for (int j = 0; j < SIZE; j++) {
            printf("%c ", tablero[i][j]);
        }
        printf("\n");
    }
}

// Función para convertir una cadena a mayúsculas
void convertirMayusculas(char palabra[]) {
    for (int i = 0; palabra[i] != '\0'; i++)
        palabra[i] = toupper(palabra[i]);
}

// Función para verificar si una palabra está en la lista oficial
int buscarPalabra(const char* palabra) {
    for (int i = 0; i < MAX_PALABRAS; i++) {
        if (strcmp(lista_palabras[i], palabra) == 0)
            return i; // Retorna índice si la encuentra
    }
    return -1; // No encontrada
}

// Función para verificar si se puede colocar una palabra
int puedeColocar(char tablero[SIZE][SIZE], const char* palabra, int fila, int col, char direccion) {
    int len = strlen(palabra);

    if (direccion == 'H') {
        if (col + len > SIZE) return 0; // Se pasa de la derecha
        for (int i = 0; i < len; i++) {
            if (tablero[fila][col + i] != ' ' && tablero[fila][col + i] != palabra[i])
                return 0;
        }
    } else if (direccion == 'V') {
        if (fila + len > SIZE) return 0; // Se pasa hacia abajo
        for (int i = 0; i < len; i++) {
            if (tablero[fila + i][col] != ' ' && tablero[fila + i][col] != palabra[i])
                return 0;
        }
    } else {
        return 0; // Dirección inválida
    }
    return 1;
}

// Función para colocar la palabra
void colocarPalabra(char tablero[SIZE][SIZE], const char* palabra, int fila, int col, char direccion) {
    int len = strlen(palabra);

    if (direccion == 'H') {
        for (int i = 0; i < len; i++)
            tablero[fila][col + i] = palabra[i];
    } else if (direccion == 'V') {
        for (int i = 0; i < len; i++)
            tablero[fila + i][col] = palabra[i];
    }
}

int main() {
    char tablero[SIZE][SIZE];
    inicializarTablero(tablero);

    char palabra[LONGITUD_MAX];
    int fila, col;
    char direccion;
    int continuar = 1;
    int palabras_insertadas = 0;

    printf("==== Bienvenido a la Cruzisopa ====\n\n");

    while (continuar) {
        imprimirTablero(tablero);
        printf("\nPalabras colocadas: %d/%d\n", palabras_insertadas, MAX_PALABRAS);

        printf("\nIngrese la palabra (o 'FIN' para terminar): ");
        scanf("%s", palabra);
        convertirMayusculas(palabra);

        if (strcmp(palabra, "FIN") == 0) {
            printf("Finalizando el programa.\n");
            break;
        }

        int indice = buscarPalabra(palabra);

        if (indice == -1) {
            printf("Error: La palabra '%s' no está en la lista permitida.\n", palabra);
            continue;
        }

        if (palabras_colocadas[indice]) {
            printf("Error: La palabra '%s' ya fue colocada anteriormente.\n", palabra);
            continue;
        }

        printf("Ingrese la fila inicial (0-9): ");
        scanf("%d", &fila);

        printf("Ingrese la columna inicial (0-9): ");
        scanf("%d", &col);

        printf("Ingrese la dirección (H = Horizontal, V = Vertical): ");
        scanf(" %c", &direccion);
        direccion = toupper(direccion);

        if (puedeColocar(tablero, palabra, fila, col, direccion)) {
            colocarPalabra(tablero, palabra, fila, col, direccion);
            palabras_colocadas[indice] = 1;
            palabras_insertadas++;
            printf("Palabra '%s' colocada exitosamente!\n", palabra);
        } else {
            printf("Error: No se puede colocar la palabra '%s' en esa posición o dirección.\n", palabra);
        }

        if (palabras_insertadas == MAX_PALABRAS) {
            printf("\n¡Felicidades! Has colocado todas las palabras.\n");
            break;
        }
    }

    printf("\nTablero final:\n");
    imprimirTablero(tablero);

    return 0;
}
