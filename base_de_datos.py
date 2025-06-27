# Base de datos

import sqlite3
import os
from colorama import Fore, Style
import datetime

# Ruta de la base de datos SQLite
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE_PATH = os.path.join(BASE_DIR, 'clientes.db')

def get_db_connection():
    """Establece una conexión a la base de datos y configura row_factory para obtener resultados como diccionarios."""
    conn = sqlite3.connect(DB_FILE_PATH)
    conn.row_factory = sqlite3.Row # Permite acceder a las columnas por nombre
    return conn

def inicializar_db():
    """Crea la tabla 'clientes' si no existe y añade la columna 'Fecha_registro' si no existe."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Nombre TEXT NOT NULL,
            Apellido TEXT NOT NULL,
            Email TEXT UNIQUE NOT NULL,
            Telefono TEXT NOT NULL,
            Fuero TEXT NOT NULL,
            Tipo_de_caso TEXT NOT NULL
        )
    ''')
    
    # Agrega la columna si no existe para actualizar la tabla
    try:
        cursor.execute("ALTER TABLE clientes ADD COLUMN Fecha_registro TEXT")
        print(Fore.GREEN + "✔️ Columna 'Fecha_registro' añadida a la tabla 'clientes'." + Style.RESET_ALL)
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            # La columna ya existe, no hacemos nada
            pass 
        else:
            # Otra excepción
            print(Fore.RED + f"❌ Error al modificar la tabla: {e}" + Style.RESET_ALL)

    conn.commit()
    conn.close()
    print(Fore.GREEN + "✔️ Base de datos SQLite inicializada o actualizada correctamente." + Style.RESET_ALL)

# Operaciones CRUD para Clientes

def insertar_cliente(nombre, apellido, email, telefono, fuero, tipo_caso):
    """Inserta un nuevo cliente en la base de datos."""
    conn = get_db_connection()
    cursor = conn.cursor()
    # Captura la fecha y hora actual para el registro
    fecha_registro = datetime.datetime.now().isoformat()
    
    try:
        cursor.execute('''
            INSERT INTO clientes (Nombre, Apellido, Email, Telefono, Fuero, Tipo_de_caso, Fecha_registro)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (nombre, apellido, email, telefono, fuero, tipo_caso, fecha_registro))
        conn.commit()
        return cursor.lastrowid # Retorna el ID del nuevo cliente
    except sqlite3.IntegrityError:
        print(Fore.RED + "❌ Error: Ya existe un cliente con este email." + Style.RESET_ALL)
        return None
    finally:
        conn.close()

def obtener_todos_los_clientes():
    """Obtiene todos los clientes de la base de datos con la fecha de registro formateada."""
    conn = get_db_connection()
    cursor = conn.cursor()
    # Selecciona todos los campos y formatea la fecha de registro para una mejor visualización
    cursor.execute('SELECT *, strftime("%d-%m-%Y %H:%M:%S", Fecha_registro) AS Fecha_registro_formateada FROM clientes ORDER BY ID ASC')
    clientes_db = [dict(row) for row in cursor.fetchall()] # Convierte sqlite3.Row a diccionario
    conn.close()
    return clientes_db

def obtener_cliente_por_id(cliente_id):
    """Obtiene un cliente por su ID, con la fecha de registro formateada."""
    conn = get_db_connection()
    cursor = conn.cursor()
    # Modificación: Agregamos strftime para formatear la fecha
    cursor.execute('SELECT *, strftime("%d-%m-%Y %H:%M:%S", Fecha_registro) AS Fecha_registro_formateada FROM clientes WHERE ID = ?', (cliente_id,))
    cliente_db = cursor.fetchone()
    conn.close()
    return dict(cliente_db) if cliente_db else None

def obtener_cliente_por_email(email):
    """Obtiene un cliente por su email, con la fecha de registro formateada."""
    conn = get_db_connection()
    cursor = conn.cursor()
    # Modificación: Agregamos strftime para formatear la fecha
    cursor.execute('SELECT *, strftime("%d-%m-%Y %H:%M:%S", Fecha_registro) AS Fecha_registro_formateada FROM clientes WHERE Email = ?', (email,))
    cliente_db = cursor.fetchone()
    conn.close()
    return dict(cliente_db) if cliente_db else None

def actualizar_cliente_db(cliente_id, nombre, apellido, email, telefono, fuero, tipo_caso):
    """Actualiza la información de un cliente en la base de datos."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            UPDATE clientes
            SET Nombre = ?, Apellido = ?, Email = ?, Telefono = ?, Fuero = ?, Tipo_de_caso = ?
            WHERE ID = ?
        ''', (nombre, apellido, email, telefono, fuero, tipo_caso, cliente_id))
        conn.commit()
        return cursor.rowcount > 0 # Retorna True si se actualizó una fila
    except sqlite3.IntegrityError:
        print(Fore.RED + "❌ Error: Ya existe un cliente con este email al intentar actualizar." + Style.RESET_ALL)
        return False
    finally:
        conn.close()

def eliminar_cliente_db(cliente_id):
    """Elimina un cliente de la base de datos por su ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM clientes WHERE ID = ?', (cliente_id,))
    conn.commit()
    conn.close()
    return cursor.rowcount > 0 # Retorna True si se eliminó una fila

def buscar_clientes_por_fuero(fuero):
    """Busca clientes por el fuero especificado."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clientes WHERE Fuero = ? ORDER BY ID ASC', (fuero,))
    clientes_db = [dict(row) for row in cursor.fetchall()] #busca todo
    conn.close()
    return clientes_db