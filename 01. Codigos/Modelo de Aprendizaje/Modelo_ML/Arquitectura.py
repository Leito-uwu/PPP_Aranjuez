import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model

def construir_modelo_inspector(input_shape=(224, 224, 3)):
    
    # 1. Base pre-entrenada (MobileNetV2)
    base_model = MobileNetV2(input_shape=input_shape, include_top=False, weights='imagenet')
    base_model.trainable = False # Congelamos conocimiento
    
    # 2. Nuestra cabeza de clasificación
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(128, activation='relu')(x)
    x = Dropout(0.2)(x) # Prevención de sobreentrenamiento
    
    # 3. Resultado (0 = Buena, 1 = Mala)
    salida = Dense(1, activation='sigmoid')(x)
    
    modelo = Model(inputs=base_model.input, outputs=salida)
    
    # 4. Compilación
    modelo.compile(optimizer='adam',
                   loss='binary_crossentropy',
                   metrics=['accuracy'])
    
    return modelo