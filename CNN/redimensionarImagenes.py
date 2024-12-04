import os
import cv2

# Ruta al dataset original
input_dir = r'C:/Users/Guido/Desktop/Devs/guidod-IA/DatasetAutomoviles'

# Ruta donde se guardará el dataset redimensionado
output_dir = r'C:/Users/Guido/Desktop/Devs/guidod-IA/DatasetRedimensionado'

# Dimensiones deseadas para las imágenes
TARGET_SIZE = (128, 128)

# Extensiones válidas de imágenes
valid_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".tiff")

# Crear el directorio de salida si no existe
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Recorrer el directorio original
for root, dirnames, filenames in os.walk(input_dir):
    # Crear la estructura de subdirectorios en el directorio de salida
    relative_path = os.path.relpath(root, input_dir)
    target_dir = os.path.join(output_dir, relative_path)

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # Procesar cada archivo en el directorio actual
    for filename in filenames:
        if filename.lower().endswith(valid_extensions):  # Filtrar imágenes
            # Ruta completa del archivo de entrada
            filepath = os.path.join(root, filename)

            # Leer la imagen
            image = cv2.imread(filepath)
            if image is not None:
                # Redimensionar la imagen en su formato original (a color)
                resized_image = cv2.resize(image, TARGET_SIZE)

                # Ruta completa para guardar la imagen redimensionada
                output_filepath = os.path.join(target_dir, filename)

                # Guardar la imagen redimensionada
                cv2.imwrite(output_filepath, resized_image)

                print(f"Imagen guardada en: {output_filepath}")
            else:
                print(f"No se pudo leer la imagen: {filepath}")

print("Redimensionamiento completado. Todas las imágenes están en:", output_dir)
