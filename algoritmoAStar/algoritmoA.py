import pygame
#Cola de prioridad para nodos vecinos 
from queue import PriorityQueue
import time

# Configuraciones iniciales
ANCHO_VENTANA = 800
VENTANA = pygame.display.set_mode((ANCHO_VENTANA, ANCHO_VENTANA))
pygame.display.set_caption("Visualización de Nodos")

# Colores (RGB)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (128, 128, 128)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
NARANJA = (255, 165, 0)
PURPURA = (128, 0, 128)

pygame.font.init()


class Nodo:
    def __init__(self, fila, col, ancho, total_filas):
        self.fila = fila
        self.col = col
        self.x = fila * ancho
        self.y = col * ancho
        self.color = BLANCO
        self.ancho = ancho
        self.total_filas = total_filas\
        #adicion de arreglo de vecinos para tener la info a la mano
        self.vecinos = [] 

    def get_pos(self):
        return self.fila, self.col

    def es_pared(self):
        return self.color == NEGRO

    def es_inicio(self):
        return self.color == NARANJA

    def es_fin(self):
        return self.color == PURPURA

    def restablecer(self):
        self.color = BLANCO

    def hacer_inicio(self):
        self.color = NARANJA

    def hacer_pared(self):
        self.color = NEGRO

    def hacer_fin(self):
        self.color = PURPURA

    def hacer_camino(self):
        self.color = VERDE

    def dibujar(self, ventana):
        pygame.draw.rect(ventana, self.color, (self.x, self.y, self.ancho, self.ancho))

    #Agregado de funcion que busca a los vecinos del nodo
    def actualizar_vecinos(self, grid):
        self.vecinos = []
        global costoDiagonal, costoOrtogonal
        #Definición de costos
        costoDiagonal = 2 
        costoOrtogonal = 1

        # Verificar vecino abajo con fila+1
        if self.fila < self.total_filas - 1 and not grid[self.fila + 1][self.col].es_pared():
            self.vecinos.append((grid[self.fila + 1][self.col], costoOrtogonal))
        # Verificar vecino arriba con fila-1
        if self.fila > 0 and not grid[self.fila - 1][self.col].es_pared():
            self.vecinos.append((grid[self.fila - 1][self.col], costoOrtogonal))
        # Verificar vecino derecha con col + 1
        if self.col < self.total_filas - 1 and not grid[self.fila][self.col + 1].es_pared():
            self.vecinos.append((grid[self.fila][self.col + 1], costoOrtogonal))
        # Verificar vecino izquierda con col-1
        if self.col > 0 and not grid[self.fila][self.col - 1].es_pared():
            self.vecinos.append((grid[self.fila][self.col - 1], costoOrtogonal))
            
        # Movimientos diagonales
        # Verificar vecino abajo derecha con fila+1 columna+1
        if self.fila < self.total_filas - 1 and self.col < self.total_filas - 1 and not grid[self.fila + 1][self.col + 1].es_pared():  
            self.vecinos.append((grid[self.fila + 1][self.col + 1], costoDiagonal))
        # Verificar vecino abajo izquierda con fila+1 columna-1
        if self.fila < self.total_filas - 1 and self.col > 0 and not grid[self.fila + 1][self.col - 1].es_pared(): 
            self.vecinos.append((grid[self.fila + 1][self.col - 1], costoDiagonal))
        # Verificar vecino arriba derecha con fila-1 columna+1
        if self.fila > 0 and self.col < self.total_filas - 1 and not grid[self.fila - 1][self.col + 1].es_pared():  # Arriba-Derecha
            self.vecinos.append((grid[self.fila - 1][self.col + 1], costoDiagonal))
        # Verificar vecino arriba izquierda con fila-1 columna-1
        if self.fila > 0 and self.col > 0 and not grid[self.fila - 1][self.col - 1].es_pared():  # Arriba-Izquierda
            self.vecinos.append((grid[self.fila - 1][self.col - 1], costoDiagonal))
    

    #Función que evita que el nodo se compare directamente con otros
    def __lt__(self, other):
        return False

def crear_grid(filas, ancho):
    grid = []
    ancho_nodo = ancho // filas
    for i in range(filas):
        grid.append([])
        for j in range(filas):
            nodo = Nodo(i, j, ancho_nodo, filas)
            grid[i].append(nodo)
    return grid

def dibujar_grid(ventana, filas, ancho):
    ancho_nodo = ancho // filas
    for i in range(filas):
        pygame.draw.line(ventana, GRIS, (0, i * ancho_nodo), (ancho, i * ancho_nodo))
        for j in range(filas):
            pygame.draw.line(ventana, GRIS, (j * ancho_nodo, 0), (j * ancho_nodo, ancho))

def dibujar(ventana, grid, filas, ancho):
    ventana.fill(BLANCO)
    for fila in grid:
        for nodo in fila:
            nodo.dibujar(ventana)

    dibujar_grid(ventana, filas, ancho)
    pygame.display.update()

def obtener_click_pos(pos, filas, ancho):
    ancho_nodo = ancho // filas
    y, x = pos
    fila = y // ancho_nodo
    col = x // ancho_nodo
    return fila, col

#Inicio implementaciones para A*
# Heurística: Estima la distancia entre dos nodos en este caso inicio y fin usando la distancia de Manhattan 
def heuristica(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

# Reconstrucción del camino más corto
def reconstruir_camino(came_from, current, draw):
    total_cost = 0
    while current in came_from:
        prev = current
        current = came_from[current]

        #Calculo costo diagonal o ortogonal
        if abs(prev.fila - current.fila) == 1 and abs(prev.col - current.col) == 1:
            total_cost += costoDiagonal  
        else:
            total_cost += costoOrtogonal

        current.color = (0, 0, 255)  # Azul para el camino más eficiente
        draw()
    mensaje = f"Costo total: {total_cost}"
    mostrar_mensaje(VENTANA, mensaje, ANCHO_VENTANA, ANCHO_VENTANA, PURPURA)

# Dibujar actualizaciones de la cuadricula
def draw(ventana, grid, filas, ancho):
    ventana.fill(BLANCO)
    for fila in grid:
        for nodo in fila:
            nodo.dibujar(ventana)
    dibujar_grid(ventana, filas, ancho)
    pygame.display.update()

# Nueva función para encapsular `draw`
def actualizar_ventana():
    draw(VENTANA, grid, FILAS, ANCHO_VENTANA)

#Mostrar mensaje de camino no encontrado
def mostrar_mensaje(ventana, mensaje, ancho, alto, color):
    fuente = pygame.font.SysFont(None, 40)
    texto = fuente.render(mensaje, True, color)
    ventana.blit(texto, ((ancho - texto.get_width()) // 2, (alto - texto.get_height()) // 2))
    pygame.display.update()
    time.sleep(2)  

#código a*
def algoritmo_a_star(draw, grid, inicio, objetivo):
    # Crear una cola de prioridad
    open_set = PriorityQueue()
    # agregar `inicio` a `open_set` con f(inicio) = h(inicio)
    open_set.put((0, inicio))
    came_from = {}  # Diccionario para rastrear el mejor camino

     # g_score[inicio] = 0
     #f_score[inicio] = h(inicio)
     #Se pone en infinito para asegurar que todos los caminos tengan menor costo.
    g_score = {nodo: float("inf") for fila in grid for nodo in fila}
    g_score[inicio] = 0  # g_score del nodo inicial es 0

    f_score = {nodo: float("inf") for fila in grid for nodo in fila}
    f_score[inicio] = heuristica(inicio.get_pos(), objetivo.get_pos())  # f_score = heurística del nodo inicial

    #Creacion de conjunto que vaya a la par de open_set y permita buscar duplicados mas eficientemente
    open_set_hash = {inicio}
    
    #While `open_set` no esté vacío:
    while not open_set.empty():  

        #Manejador de eventos escuchando al usuario
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Obtener el nodo con el menor f_score
        current = open_set.get()[1]
        open_set_hash.remove(current)

        print(f"Procesando nodo {current.get_pos()} con g_score={g_score[current]} y f_score={f_score[current]}")

        # Si hemos llegado al nodo final, reconstruimos el camino
        if current == objetivo:
            reconstruir_camino(came_from, objetivo, draw)
            objetivo.hacer_fin()
            inicio.hacer_inicio()
            return True

        # Explorar los vecinos del nodo actual
        for vecino, costo  in current.vecinos:
            tentative_g_score = g_score[current] + costo  # Costo acumulado para llegar al vecino

            # Si encontramos un mejor camino hacia el vecino
            if tentative_g_score < g_score[vecino]:
                came_from[vecino] = current  # Registrar el mejor camino
                g_score[vecino] = tentative_g_score
                f_score[vecino] = g_score[vecino] + heuristica(vecino.get_pos(), objetivo.get_pos())

                # Si el vecino no está en open_set, lo agregamos
                if vecino not in open_set_hash:
                    open_set.put((f_score[vecino], vecino))
                    open_set_hash.add(vecino)

        draw()  # Actualizar la visualización

        time.sleep(0.2)  # Añadimos un retraso para visualizar el progreso

        if current != inicio:
            current.hacer_camino()  # Marcar el nodo como procesado

    mostrar_mensaje(VENTANA, "No se encontró un camino", ANCHO_VENTANA, ANCHO_VENTANA, ROJO)
    return False  # Si no hay camino, devolver False

#FUNCIÓN PRINCIPAL
def main(ventana, ancho):
    global grid, FILAS
    FILAS = 10
    grid = crear_grid(FILAS, ancho)

    inicio = None
    fin = None

    corriendo = True

    while corriendo:
        dibujar(ventana, grid, FILAS, ancho)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False

            if pygame.mouse.get_pressed()[0]:  # Click izquierdo
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, FILAS, ancho)
                nodo = grid[fila][col]
                if not inicio and nodo != fin:
                    inicio = nodo
                    inicio.hacer_inicio()

                elif not fin and nodo != inicio:
                    fin = nodo
                    fin.hacer_fin()

                elif nodo != fin and nodo != inicio:
                    nodo.hacer_pared()

            elif pygame.mouse.get_pressed()[2]:  # Click derecho
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, FILAS, ancho)
                nodo = grid[fila][col]
                nodo.restablecer()
                if nodo == inicio:
                    inicio = None
                elif nodo == fin:
                    fin = None

            #Inicio de algoritmo a* con la tecla spacio
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and inicio and fin:
                    for fila in grid:
                        for nodo in fila:
                            nodo.actualizar_vecinos(grid)

                    algoritmo_a_star(actualizar_ventana, grid, inicio, fin)

    pygame.quit()

main(VENTANA, ANCHO_VENTANA)