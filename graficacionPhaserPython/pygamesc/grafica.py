
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Cargar los datos desde el CSV especificando que la primera fila es un encabezado
df = pd.read_csv('/home/likcos/testphaser.csv', header=None, names=['velocidad_bala', 'distancia', 'salto_hecho'], dtype=float)

# Crear la figura 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
# Graficar puntos con salto_hecho=0
ax.scatter(df[df['salto_hecho'] == 0]['velocidad_bala'], df[df['salto_hecho'] == 0]['distancia'], df[df['salto_hecho'] == 0]['salto_hecho'],
           c='blue', marker='o', label='salto_hecho=0')
# Graficar puntos con salto_hecho=1
ax.scatter(df[df['salto_hecho'] == 1]['velocidad_bala'], df[df['salto_hecho'] == 1]['distancia'], df[df['salto_hecho'] == 1]['salto_hecho'],
           c='red', marker='x', label='salto_hecho=1')
# Etiquetas de los ejes
ax.set_xlabel('velocidad_bala')
ax.set_ylabel('distancia')
ax.set_zlabel('salto_hecho')
# Mostrar leyenda
ax.legend()
# Mostrar el gráfico
plt.show()




