import pygame
import random
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_graphviz
import graphviz
from mpl_toolkits.mplot3d import Axes3D
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split
import numpy as np
from tensorflow.keras.optimizers import Adam

# Inicializar Pygame
pygame.init()

# Dimensiones de la pantalla
w, h = 800, 400
pantalla = pygame.display.set_mode((w, h))
pygame.display.set_caption("Juego: Disparo de Bala, Salto, Nave y Menú")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Variables del jugador, bala, nave, fondo, etc.
jugador = None
bala = None
fondo = None
nave = None
menu = None

# Variables de salto
salto = False
salto_altura = 15  # Velocidad inicial de salto
gravedad = 1
en_suelo = True

# Variables de pausa y menú
pausa = False
fuente = pygame.font.SysFont('Arial', 24)
menu_activo = True
modo_auto = False  # Indica si el modo de juego es automático
mlp_clf = None
modo_mlp = False 

# Lista para guardar los datos de velocidad, distancia y salto (target)
datos_modelo = []

# Cargar las imágenes
jugador_frames = [
    pygame.image.load('assets/sprites/mono_frame_1.png'),
    pygame.image.load('assets/sprites/mono_frame_2.png'),
    pygame.image.load('assets/sprites/mono_frame_3.png'),
    pygame.image.load('assets/sprites/mono_frame_4.png')
]

bala_img = pygame.image.load('assets/sprites/purple_ball.png')
fondo_img = pygame.image.load('assets/game/fondo2.png')
nave_img = pygame.image.load('assets/game/ufo.png')
menu_img = pygame.image.load('assets/game/menu.png')

# Escalar la imagen de fondo para que coincida con el tamaño de la pantalla
fondo_img = pygame.transform.scale(fondo_img, (w, h))

# Crear el rectángulo del jugador y de la bala
jugador = pygame.Rect(50, h - 100, 32, 48)
bala = pygame.Rect(w - 50, h - 90, 16, 16)
nave = pygame.Rect(w - 100, h - 100, 64, 64)
menu_rect = pygame.Rect(w // 2 - 135, h // 2 - 90, 270, 180)  # Tamaño del menú

# Variables para la animación del jugador
current_frame = 0
frame_speed = 10 
frame_count = 0

# Variables para la bala
velocidad_bala = -10 
bala_disparada = False

# Variables para el fondo en movimiento
fondo_x1 = 0
fondo_x2 = w

# Función para disparar la bala
def disparar_bala():
    global bala_disparada, velocidad_bala
    if not bala_disparada:
        velocidad_bala = random.randint(-8, -3)  
        bala_disparada = True

# Función para reiniciar la posición de la bala
def reset_bala():
    global bala, bala_disparada
    bala.x = w - 50 
    bala_disparada = False

# Función para manejar el salto
def manejar_salto():
    global jugador, salto, salto_altura, gravedad, en_suelo

    if salto:
        jugador.y -= salto_altura  
        salto_altura -= gravedad  

        # Si el jugador llega al suelo, detener el salto
        if jugador.y >= h - 100:
            jugador.y = h - 100
            salto = False
            salto_altura = 15  
            en_suelo = True

# Función para actualizar el juego
def update():
    global bala, velocidad_bala, current_frame, frame_count, fondo_x1, fondo_x2

    # Mover el fondo
    fondo_x1 -= 1
    fondo_x2 -= 1

    # Si el primer fondo sale de la pantalla, lo movemos detrás del segundo
    if fondo_x1 <= -w:
        fondo_x1 = w

    # Si el segundo fondo sale de la pantalla, lo movemos detrás del primero
    if fondo_x2 <= -w:
        fondo_x2 = w

    # Dibujar los fondos
    pantalla.blit(fondo_img, (fondo_x1, 0))
    pantalla.blit(fondo_img, (fondo_x2, 0))

    # Animación del jugador
    frame_count += 1
    if frame_count >= frame_speed:
        current_frame = (current_frame + 1) % len(jugador_frames)
        frame_count = 0

    # Dibujar el jugador con la animación
    pantalla.blit(jugador_frames[current_frame], (jugador.x, jugador.y))

    # Dibujar la nave
    pantalla.blit(nave_img, (nave.x, nave.y))

    # Mover y dibujar la bala
    if bala_disparada:
        bala.x += velocidad_bala

    # Si la bala sale de la pantalla, reiniciar su posición
    if bala.x < 0:
        reset_bala()

    pantalla.blit(bala_img, (bala.x, bala.y))

    # Colisión entre la bala y el jugador
    if jugador.colliderect(bala):
        print("Colisión detectada!")
        reiniciar_juego()  # Terminar el juego y mostrar el menú

# Función para guardar datos del modelo en modo manual
def guardar_datos():
    global jugador, bala, velocidad_bala, salto
    distancia = abs(jugador.x - bala.x)
    salto_hecho = 1 if salto else 0  # 1 si saltó, 0 si no saltó
    # Guardar velocidad de la bala, distancia al jugador y si saltó o no
    datos_modelo.append((velocidad_bala, distancia, salto_hecho))

# Función para pausar el juego y guardar los datos
def pausa_juego():
    global pausa
    pausa = not pausa
    if pausa:
        print("Juego pausado. Datos registrados hasta ahora:", datos_modelo)
    else:
        print("Juego reanudado.")

# Función para mostrar el menú y seleccionar el modo de juego
def mostrar_menu():
    global menu_activo, modo_auto, datos_modelo, clf, modo_mlp, mlp_clf
    pantalla.fill(NEGRO)
    lineas_menu = [
        "Menu:",
        "'A' para auto con arboles",
        "'R' para auto con redes",
        "'M' para Manual",
        "'G' para gráfica",
        "'S' Dentro del juego para regresar al menu",
        "'Q' para Salir"
    ]
    
    x_inicial = w // 4
    y_inicial = h // 3
    espaciado = 30
    for i, linea in enumerate(lineas_menu):
        texto = fuente.render(linea, True, BLANCO)
        pantalla.blit(texto, (x_inicial, y_inicial + i * espaciado))
    
    pygame.display.flip()

    while menu_activo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_a:
                    if len(datos_modelo) == 0:
                        print("No hay datos para entrenar el modelo.")
                        menu_activo = True  
                    else:
                        modo_auto = True
                        menu_activo = False
                        modo_mlp = False
                        arbolDec()  
                        jugador.y = h - 100 
                        salto = False 
                        en_suelo = True  
                        print("Modo Automático: Entrenando modelo...")
                        arbolDec()
                
                elif evento.key == pygame.K_r:
                    if len(datos_modelo) == 0:
                        print("No hay datos para entrenar el modelo.")
                        menu_activo = True
                    else:
                        modo_auto = True
                        modo_mlp = True
                        menu_activo = False
                        entrenar_mlp()
                        print("Modo Automático (MLP): Entrenando modelo...")
                elif evento.key == pygame.K_m:
                    modo_auto = False
                    menu_activo = False
                    datos_modelo = []
                    jugador.y = h - 100  # Restablecer la posición en el suelo
                    salto = False  # Asegurarse de que no haya salto pendiente
                    en_suelo = True
                elif evento.key == pygame.K_q:
                    print("Juego terminado. Datos recopilados:", datos_modelo)
                    pygame.quit()
                    exit()
                elif evento.key == pygame.K_g:
                    graficar()
                    pygame.quit()

#Funcion redes neuronales multicapa
def entrenar_mlp():
    global mlp_clf
    global mlp_model, datos_modelo
    if len(datos_modelo) == 0:
        print("No hay datos suficientes para entrenar el modelo MLP.")
        return

    dataset = pd.DataFrame(datos_modelo, columns=['velocidad_bala', 'distancia', 'salto_hecho'])
    X = dataset.iloc[:, :2].values  
    y = dataset.iloc[:, 2].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    mlp_model = Sequential([
        Dense(12, input_dim=2, activation='swish'),
        Dense(8, input_dim=2, activation='swish'),
        Dense(1, activation='sigmoid')
    ])
    mlp_model.compile(optimizer=Adam(learning_rate=0.01), loss='binary_crossentropy', metrics=['accuracy'])

    mlp_model.fit(X_train, y_train, epochs=100, batch_size=32, verbose=1)

    loss, accuracy = mlp_model.evaluate(X_test, y_test, verbose=0)
    print(f"Precisión en el conjunto de prueba: {accuracy:.2f}")

#Función decision Tree
def arbolDec():
    global clf
    dataset = pd.DataFrame(datos_modelo, columns=['velocidad_bala', 'distancia', 'salto_hecho'])

    X = dataset.iloc[:, :2]  
    y = dataset.iloc[:, 2] 

    # Crear el clasificador de Árbol de Decisión
    clf = DecisionTreeClassifier()

    # Entrenar el modelo
    clf.fit(X, y)
    # # Exportar el árbol de decisión en formato DOT para su visualización
    # dot_data = export_graphviz(clf, out_file=None, 
    #                         feature_names=['Feature 1', 'Feature 2'],  
    #                         class_names=['Clase 0', 'Clase 1'],  
    #                         filled=True, rounded=True,  
    #                         special_characters=True)  

    # # Crear el gráfico con graphviz
    # graph = graphviz.Source(dot_data)

    # # Mostrar el gráfico
    # graph.view()

#Funcion para graficar

def graficar():
    # Crear un DataFrame a partir de los datos existentes
    df = pd.DataFrame(datos_modelo, columns=['velocidad_bala', 'distancia', 'salto_hecho'])

    # Crear una figura
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    # Graficar los datos
    ax.scatter(df["Velocidad de Bala"], df["Distancia"], df["Salto"])

    # Etiquetas de los ejes
    ax.set_xlabel("Velocidad de Bala")
    ax.set_ylabel("Distancia")
    ax.set_zlabel("Salto")
    # Mostrar el gráfico
    plt.show()

# Función para reiniciar el juego tras la colisión
def reiniciar_juego():
    global menu_activo, jugador, bala, nave, bala_disparada, salto, en_suelo, modo_auto
    menu_activo = True  # Activar de nuevo el menú
    jugador.x, jugador.y = 50, h - 100  # Reiniciar posición del jugador
    bala.x = w - 50  # Reiniciar posición de la bala
    nave.x, nave.y = w - 100, h - 100  # Reiniciar posición de la nave
    bala_disparada = False
    salto = False
    en_suelo = True
    # Mostrar los datos recopilados hasta el momento
    if(modo_auto == False): 
        print("Datos recopilados para el modelo: ", datos_modelo)
    mostrar_menu()  # Mostrar el menú de nuevo para seleccionar modo

def arbol_decision_predict():
    global clf
    # Usar el modelo entrenado para predecir el salto
    # Supongamos que tenemos las variables velocidad_bala y distancia en este punto
    datos_actuales = [velocidad_bala, abs(jugador.x - bala.x)]  # Datos a predecir (velocidad y distancia)
    prediccion = clf.predict([datos_actuales])  # clf es el clasificador de Árbol de Decisión entrenado
    return prediccion[0]  # Devuelve 1 si debe saltar, 0 si no

def mlp_predict():
    global mlp_model
    if mlp_model is None:
        print("El modelo MLP no está entrenado.")
        return 0

    # Preparar los datos de entrada
    datos_actuales = np.array([[velocidad_bala, abs(jugador.x - bala.x)]])
    prediccion = mlp_model.predict(datos_actuales)
    return int(prediccion[0][0] > 0.5)  # Devuelve 1 si la probabilidad > 0.5, 0 si n


def main():
    global salto, en_suelo, bala_disparada, modo_auto, clf, modo_mlp, mlp_clf


    reloj = pygame.time.Clock()
    mostrar_menu()  # Mostrar el menú al inicio
    correr = True

    while correr:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                correr = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and en_suelo and not pausa:  # Detectar la tecla espacio para saltar
                    salto = True
                    en_suelo = False
                if evento.key == pygame.K_p:  # Presiona 'p' para pausar el juego
                    pausa_juego()
                if evento.key == pygame.K_q:  # Presiona 'q' para terminar el juego
                    print("Juego terminado. Datos recopilados:", datos_modelo)
                    pygame.quit()
                    exit()
                if evento.key == pygame.K_s:  # Presiona 'e' para salir y mostrar los datos
                    reiniciar_juego()

        if not pausa:
            # Modo automático: el árbol de decisión controla el salto
            if modo_auto:
                # Usamos el árbol de decisión para predecir si saltar
                if modo_mlp:
                    prediccion = mlp_predict()
                else:
                    prediccion = arbol_decision_predict()

                if prediccion == 1 and en_suelo:  # Si la predicción es 1, significa que el salto debe hacerse
                    salto = True
                    en_suelo = False
                if salto:
                    manejar_salto()
            else:
                # Modo manual: el jugador controla el salto
                if salto:
                    manejar_salto()

            # Guardar los datos si estamos en modo manual
            if not modo_auto:
                guardar_datos()

            # Actualizar el juego
            if not bala_disparada:
                disparar_bala()
            update()

        # Actualizar la pantalla
        pygame.display.flip()
        reloj.tick(30)  # Limitar el juego a 30 FPS

    pygame.quit()

if __name__ == "__main__":
    main()