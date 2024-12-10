import torch
import numpy as np
from PIL import Image
from skimage.transform import resize
from keras.models import load_model

# Poner la ruta a la imagen de prueba
input_image_path = "C:/Users/Guido/Desktop/Devs/IA/guidod-IA/PROYECTO3CNN/cars dataset/ImagenesPrueba/prueba19.jpg"

# Modelo YOLOv5 para detección
model_yolo = torch.hub.load('ultralytics/yolov5', 'yolov5m', trust_repo=True).to('cuda')

# Modelo de clasificación de riesgo
riesgo_model = load_model('automovilesV2.h5')
sriesgos = ['AudiSUV', 'DodgeChallenger', 'FordF150XLT', 'JeepWranglerSahara', 'ToyotaCamrySE']  # Etiquetas reales

# Clases relevantes en COCO para vehículos completos
vehicle_classes = [2, 5, 7]  # 2: car, 5: bus, 7: truck

try:
    # Cargar imagen
    img = Image.open(input_image_path).convert('RGB')
    img_width, img_height = img.size
    img_area = img_width * img_height

    # Realizar la detección con YOLOv5
    results = model_yolo(img)
    detections = results.xyxy[0]

    # Buscar la detección más grande que cumpla con los criterios
    largest_box = None
    largest_box_area = 0

    if detections is not None and len(detections) > 0:
        for det in detections:
            xmin, ymin, xmax, ymax, conf, cls = det.tolist()
            cls = int(cls)
            confidence = float(conf)

            box_width = xmax - xmin
            box_height = ymax - ymin
            box_area = box_width * box_height

            #criterios como el dataset, 65 de confianza minimo, se puede cambiar para pruebas
            if cls in vehicle_classes and confidence >= 0.65:
                #Al menos el 50% del area de la imagen, igual se puede cambiar
                if box_area > largest_box_area and box_area / img_area >= 0.5:
                    largest_box_area = box_area
                    largest_box = (xmin, ymin, xmax, ymax)

    if largest_box is not None:
        # Recortar la detección más grande en memoria
        xmin, ymin, xmax, ymax = map(int, largest_box)
        cropped_img = img.crop((xmin, ymin, xmax, ymax))

        # Preprocesar para el modelo riesgo_model
        image_array = np.array(cropped_img)
        image_resized = resize(image_array, (28, 21), anti_aliasing=True, clip=False, preserve_range=True)
        test_X = np.expand_dims(image_resized, axis=0).astype('float32') / 255.0

        # Predicción con riesgo_model
        predicted_class = riesgo_model.predict(test_X)
        predicted_label = sriesgos[np.argmax(predicted_class)]
        print(f"Predicción: {predicted_label}")
    else:
        print("No se detectaron vehículos que cumplan con los criterios.")
except Exception as e:
    print(f"Error procesando la imagen: {e}")
