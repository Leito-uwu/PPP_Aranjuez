import tensorflow as tf

def cargar_datasets(ruta_dataset, tamano_lote=32, tamano_imagen=(224, 224)):
    
    train_ds = tf.keras.utils.image_dataset_from_directory(
        ruta_dataset,
        validation_split=0.2,       ## Se usa un 20% del Dataset para la validación del código
        subset="training",
        seed=123,
        image_size=tamano_imagen,
        batch_size=tamano_lote,
        color_mode='rgb' 
    )

    val_ds = tf.keras.utils.image_dataset_from_directory(
        ruta_dataset,
        validation_split=0.2,
        subset="validation",
        seed=123,
        image_size=tamano_imagen,
        batch_size=tamano_lote,
        color_mode='rgb'
    )

    # Optimización de la Memoria

    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

    return train_ds, val_ds