import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Cargar el archivo CSV
data = pd.read_csv('datos50seg101.csv')  # Cambia la ruta a tu archivo

# Crear una tabla pivotada para el heatmap
heatmap_data = data.pivot_table(index='Desplazamiento Bala', columns='Velocidad Bala', values='Estatus', aggfunc='mean')

# Crear el heatmap para visualizar patrones de decisión
plt.figure(figsize=(12, 8))
sns.heatmap(heatmap_data, cmap='coolwarm', cbar=True)
plt.title('Heatmap de Decisiones: Frecuencia de Saltos 50 seg')
plt.xlabel('Velocidad Bala')
plt.ylabel('Desplazamiento Bala')

# Mostrar el heatmap
plt.show()

