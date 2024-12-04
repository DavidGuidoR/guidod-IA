import numpy as np
import os
import re
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import keras
import tensorflow as tf
from tensorflow.keras.utils import to_categorical
from keras.models import Sequential,Model
from tensorflow.keras.layers import Input
from keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.layers import (
    BatchNormalization, SeparableConv2D, MaxPooling2D, Activation, Flatten, Dropout, Dense, Conv2D
)
from keras.layers import LeakyReLU

dirname = os.path.join(os.getcwd(),'C:/Users/Guido/Desktop/Devs/guidod-IA/DatasetRedimensionado')
imgpath = dirname + os.sep 
images = []
directories = []
dircount = []
prevRoot=''
cant=0


print("leyendo imagenes de ",imgpath)

for root, dirnames, filenames in os.walk(imgpath):
    for filename in filenames:
        if re.search(r".(jpg|jpeg|png|bmp|tiff)$", filename):
            cant=cant+1
            filepath = os.path.join(root, filename)
            image = plt.imread(filepath)
            if(len(image.shape)==3):
                
                images.append(image)
            b = "Leyendo..." + str(cant)
#cant>0 para evitar conteo del directorio root
    if  cant>0 and prevRoot !=root:
        directories.append(root)
        dircount.append(cant)
        prevRoot=root
        cant=0
        

print(directories)
print('Directorios leidos:',len(directories))
print("Imagenes en cada directorio", dircount)
print('suma Total de imagenes en subdirs:',sum(dircount))

#Etiquetado de imagenes
labels=[]
indice=0
for cantidad in dircount:
    for i in range(cantidad):
        labels.append(indice)
    indice=indice+1
print("Cantidad etiquetas creadas: ",len(labels))

#Impresiones etiqueta y directorio
sriesgos=[]
indice=0
for directorio in directories:
    name = directorio.split(os.sep)
    print(indice , name[len(name)-1])
    sriesgos.append(name[len(name)-1])
    indice=indice+1

#Conversiones a numpy para que la libreria lo pueda entender
y = np.array(labels)
#nota: las imagenes deben ser del mismo tamaño o la conversion producira un error
X = np.array(images, dtype=np.uint8)

classes = np.unique(y)
nClasses = len(classes)
print('Total number of outputs : ', nClasses)
print('Output classes : ', classes)

#Division en 80% datos de entrenamiento y 20% de prueba
train_X,test_X,train_Y,test_Y = train_test_split(X,y,test_size=0.2)
print('Training data shape : ', train_X.shape, train_Y.shape)
print('Testing data shape : ', test_X.shape, test_Y.shape)

plt.figure(figsize=[5, 5])

# Mostrar la primera imagen del conjunto de entrenamiento
plt.subplot(121)
plt.imshow(train_X[0], cmap='gray') 
plt.title("Vehicle label : {}".format(train_Y[0]))

# Mostrar la primera imagen del conjunto de prueba
plt.subplot(122)
plt.imshow(test_X[0], cmap='gray')  
plt.title("Vehicle label : {}".format(test_Y[0]))

plt.show()

#Normalización de las imagenes en formato float32
train_X = train_X.astype('float32')
test_X = test_X.astype('float32')
train_X = train_X/255.
test_X = test_X/255.
plt.imshow(test_X[0,:,:])

plt.show()

#Conversiones formato one_hot 
train_Y_one_hot = to_categorical(train_Y)
test_Y_one_hot = to_categorical(test_Y)
print('Original label:', train_Y[0])
print('After conversion to one-hot:', train_Y_one_hot[0])

#Comienzos del entrenamiento del modelo
#Mezclar todo y crear los grupos de entrenamiento y testing
train_X,valid_X,train_label,valid_label = train_test_split(train_X, train_Y_one_hot, test_size=0.2, random_state=13)

#Comprobación division de datos
print(train_X.shape,valid_X.shape,train_label.shape,valid_label.shape)

