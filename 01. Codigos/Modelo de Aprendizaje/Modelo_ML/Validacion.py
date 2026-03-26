import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report

etiquetas_reales = []
predicciones_ia = []

# Recortar el lote de Validacion
for imagenes, etiquetas in val_ds:
    
    preds = modelo_inspector.predict(imagenes, verbose=0)
    etiquetas_reales.extend(etiquetas.numpy())
    preds_binarias = [1 if p > 0.5 else 0 for p in preds.flatten()]
    predicciones_ia.extend(preds_binarias)

# Matriz
matriz = confusion_matrix(etiquetas_reales, predicciones_ia)

plt.figure(figsize=(7, 6))
nombres_clases = ['Buenas (0)', 'Malas (1)']

sns.heatmap(matriz, annot=True, fmt='d', cmap='Blues', 
            xticklabels=nombres_clases, 
            yticklabels=nombres_clases,
            annot_kws={"size": 14}) # Tamaño de los números

# Títulos y etiquetas adaptadas para la línea de producción
plt.title('Matriz de Confusión: Inspección de Botellas', fontweight='bold', pad=15)
plt.ylabel('ESTADO REAL EN LÍNEA', fontweight='bold')
plt.xlabel('LO QUE DETECTÓ', fontweight='bold')
plt.tight_layout()
plt.show()

# Imprimir el resumen estadístico
print("\n REPORTE DE PRECISIÓN:\n")
print(classification_report(etiquetas_reales, predicciones_ia, target_names=nombres_clases))