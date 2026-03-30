import sqlite3
from datetime import datetime
import os

def obtener_ruta_bd():
    # Guarda el archivo en la misma carpeta que este script
    ruta_script = os.path.dirname(__file__)
    return os.path.join(ruta_script, "produccion_aranjuez.db")

def inicializar_bd_produccion():
    conexion = sqlite3.connect(obtener_ruta_bd())
    cursor = conexion.cursor()
    
    # Creamos la tabla con la regla de un registro único por día y por formato
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produccion_diaria (
            fecha TEXT,
            tipo_botella TEXT,
            buenas INTEGER,
            malas INTEGER,
            UNIQUE(fecha, tipo_botella) 
        )
    ''')
    conexion.commit()
    conexion.close()

def registrar_botella(tipo_botella, estado_inspeccion):
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")
    
    incremento_buenas = 1 if estado_inspeccion == "BUENA" else 0
    incremento_malas = 1 if estado_inspeccion == "MALA" else 0

    conexion = sqlite3.connect(obtener_ruta_bd())
    cursor = conexion.cursor()

    # Comando UPSERT: Inserta si es nuevo, suma si ya existe
    cursor.execute('''
        INSERT INTO produccion_diaria (fecha, tipo_botella, buenas, malas)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(fecha, tipo_botella) DO UPDATE SET
            buenas = produccion_diaria.buenas + excluded.buenas,
            malas = produccion_diaria.malas + excluded.malas
    ''', (fecha_hoy, tipo_botella, incremento_buenas, incremento_malas))
    
    conexion.commit()
    conexion.close()

def obtener_registros(): # <--- ESTA ES LA FUNCIÓN QUE PYTHON NO ENCONTRABA
    """Devuelve todos los registros de la base de datos para mostrarlos en la tabla"""
    conexion = sqlite3.connect(obtener_ruta_bd())
    cursor = conexion.cursor()
    cursor.execute("SELECT fecha, tipo_botella, buenas, malas FROM produccion_diaria ORDER BY fecha DESC")
    datos = cursor.fetchall()
    conexion.close()
    return datos

# Inicializamos la base de datos apenas se importe este archivo
inicializar_bd_produccion()