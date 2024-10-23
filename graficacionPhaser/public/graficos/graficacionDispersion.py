import pandas as pd
import matplotlib.pyplot as plt

# Cargar el archivo CSV
data = pd.read_csv('datos50seg101.csv')  # Cambia esta ruta a la ubicación de tu archivo

# Crear un gráfico de dispersión para visualizar los datos con separabilidad por estatus
plt.figure(figsize=(10, 6))

# Separar los datos por estatus
data_0 = data[data['Estatus'] == 0]
data_1 = data[data['Estatus'] == 1]

# Graficar puntos con diferentes colores para cada estatus
plt.scatter(data_0['Desplazamiento Bala'], data_0['Velocidad Bala'], color='blue', label='Estatus 0', alpha=0.6)
plt.scatter(data_1['Desplazamiento Bala'], data_1['Velocidad Bala'], color='red', label='Estatus 1', alpha=0.6)

# Añadir etiquetas y título
plt.xlabel('Desplazamiento Bala')
plt.ylabel('Velocidad Bala')
plt.title('Gráfico de Dispersión: Separación por Estatus 50 seg')
plt.legend()
plt.grid(True)

# Mostrar el gráfico
plt.show()
