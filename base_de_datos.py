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
    """
    Crea la tabla 'clientes' con todas sus columnas si no existe,
    y añade las columnas que se hayan agregado en actualizaciones posteriores.
    """
    conn = None # Inicializa conn a None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Nombre TEXT NOT NULL,
                Apellido TEXT NOT NULL,
                Edad INTEGER,
                Email TEXT UNIQUE NOT NULL,
                Telefono TEXT NOT NULL,
                Fuero TEXT NOT NULL,
                Tipo_de_caso TEXT NOT NULL,
                Fecha_registro TEXT
            )
        ''')
        
        # Lógica de ALTER TABLE para compatibilidad con bases de datos antiguas
        # Esto asegura que las columnas se añadan si el usuario tiene una versión anterior de la DB.
        try:
            cursor.execute("ALTER TABLE clientes ADD COLUMN Fecha_registro TEXT")
        except sqlite3.OperationalError: pass # Columna ya existe

        try:
            cursor.execute("ALTER TABLE clientes ADD COLUMN Edad INTEGER") 
        except sqlite3.OperationalError: pass # Columna ya existe
        
        conn.commit()
        print(Fore.GREEN + "✔️ Base de datos SQLite inicializada o actualizada correctamente." + Style.RESET_ALL)
    except sqlite3.Error as e:
        print(Fore.RED + f"❌ Error al inicializar la base de datos: {e}" + Style.RESET_ALL)
    finally:
        if conn:
            conn.close()

# Operaciones CRUD para Clientes

def insertar_cliente(nombre, apellido, edad, email, telefono, fuero, tipo_caso):
    """Inserta un nuevo cliente en la base de datos."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        fecha_registro = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        
        cursor.execute('''
            INSERT INTO clientes (Nombre, Apellido, Edad, Email, Telefono, Fuero, Tipo_de_caso, Fecha_registro)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (nombre, apellido, edad, email, telefono, fuero, tipo_caso, fecha_registro))
        conn.commit()
        return cursor.lastrowid # Retorna el ID del nuevo cliente
    except sqlite3.IntegrityError:
        print(Fore.RED + "❌ Error: Ya existe un cliente con este email." + Style.RESET_ALL)
        return None
    except sqlite3.Error as e: # Captura otros errores de SQLite
        print(Fore.RED + f"❌ Error de base de datos al insertar cliente: {e}" + Style.RESET_ALL)
        return None
    finally:
        if conn:
            conn.close()

def obtener_todos_los_clientes():
    """Obtiene todos los clientes de la base de datos con la fecha de registro formateada."""
    conn = None
    clientes_db = []
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Selecciona todos los campos y formatea la fecha de registro para una mejor visualización
        cursor.execute('SELECT *, strftime("%d-%m-%Y %H:%M:%S", Fecha_registro) AS Fecha_registro_formateada FROM clientes ORDER BY ID ASC')
        clientes_db = [dict(row) for row in cursor.fetchall()] # Convierte sqlite3.Row a diccionario
    except sqlite3.Error as e:
        print(Fore.RED + f"❌ Error de base de datos al obtener todos los clientes: {e}" + Style.RESET_ALL)
    finally:
        if conn:
            conn.close()
    return clientes_db

def obtener_cliente_por_id(cliente_id):
    """Obtiene un cliente por su ID, con la fecha de registro formateada."""
    conn = None
    cliente_db = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Modificación: Agregamos strftime para formatear la fecha
        cursor.execute('SELECT *, strftime("%d-%m-%Y %H:%M:%S", Fecha_registro) AS Fecha_registro_formateada FROM clientes WHERE ID = ?', (cliente_id,))
        cliente_db = cursor.fetchone()
    except sqlite3.Error as e:
        print(Fore.RED + f"❌ Error de base de datos al obtener cliente por ID: {e}" + Style.RESET_ALL)
    finally:
        if conn:
            conn.close()
    return dict(cliente_db) if cliente_db else None

def obtener_cliente_por_email(email):
    """Obtiene un cliente por su email, con la fecha de registro formateada."""
    conn = None
    cliente_db = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Modificación: Agregamos strftime para formatear la fecha
        cursor.execute('SELECT *, strftime("%d-%m-%Y %H:%M:%S", Fecha_registro) AS Fecha_registro_formateada FROM clientes WHERE Email = ?', (email,))
        cliente_db = cursor.fetchone()
    except sqlite3.Error as e:
        print(Fore.RED + f"❌ Error de base de datos al obtener cliente por Email: {e}" + Style.RESET_ALL)
    finally:
        if conn:
            conn.close()
    return dict(cliente_db) if cliente_db else None

def actualizar_cliente_db(cliente_id, nombre, apellido, edad, email, telefono, fuero, tipo_caso):
    """Actualiza la información de un cliente en la base de datos."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE clientes
            SET Nombre = ?, Apellido = ?, Edad = ?, Email = ?, Telefono = ?, Fuero = ?, Tipo_de_caso = ?
            WHERE ID = ?
        ''', (nombre, apellido, edad, email, telefono, fuero, tipo_caso, cliente_id))
        conn.commit()
        return cursor.rowcount > 0 # Retorna True si se actualizó una fila
    except sqlite3.IntegrityError:
        print(Fore.RED + "❌ Error: Ya existe un cliente con este email al intentar actualizar." + Style.RESET_ALL)
        return False
    except sqlite3.Error as e:
        print(Fore.RED + f"❌ Error de base de datos al actualizar cliente: {e}" + Style.RESET_ALL)
        return False
    finally:
        if conn:
            conn.close()

def eliminar_cliente_db(cliente_id):
    """Elimina un cliente de la base de datos por su ID."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM clientes WHERE ID = ?', (cliente_id,))
        conn.commit()
        return cursor.rowcount > 0 # Retorna True si se eliminó una fila
    except sqlite3.Error as e:
        print(Fore.RED + f"❌ Error de base de datos al eliminar cliente: {e}" + Style.RESET_ALL)
        return False
    finally:
        if conn:
            conn.close()

def buscar_clientes_por_fuero(fuero):
    """Busca clientes por el fuero especificado."""
    conn = None
    clientes_db = []
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT *, strftime("%d-%m-%Y %H:%M:%S", Fecha_registro) AS Fecha_registro_formateada FROM clientes WHERE Fuero = ? ORDER BY ID ASC', (fuero,))
        clientes_db = [dict(row) for row in cursor.fetchall()]
    except sqlite3.Error as e:
        print(Fore.RED + f"❌ Error de base de datos al buscar clientes por fuero: {e}" + Style.RESET_ALL)
    finally:
        if conn:
            conn.close()
    return clientes_db
    
# filtrar por edad
def obtener_clientes_mayores_de_edad():
    """Obtiene todos los clientes con 18 años o más."""
    conn = None
    clientes_db = []
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT *, strftime("%d-%m-%Y %H:%M:%S", Fecha_registro) AS Fecha_registro_formateada FROM clientes WHERE Edad >= 18 ORDER BY ID ASC')
        clientes_db = [dict(row) for row in cursor.fetchall()]
    except sqlite3.Error as e:
        print(Fore.RED + f"❌ Error de base de datos al obtener clientes mayores de edad: {e}" + Style.RESET_ALL)
    finally:
        if conn:
            conn.close()
    return clientes_db

def obtener_clientes_menores_de_edad():
    """Obtiene todos los clientes menores de 18 años."""
    conn = None
    clientes_db = []
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT *, strftime("%d-%m-%Y %H:%M:%S", Fecha_registro) AS Fecha_registro_formateada FROM clientes WHERE Edad < 18 ORDER BY ID ASC')
        clientes_db = [dict(row) for row in cursor.fetchall()]
    except sqlite3.Error as e:
        print(Fore.RED + f"❌ Error de base de datos al obtener clientes menores de edad: {e}" + Style.RESET_ALL)
    finally:
        if conn:
            conn.close()
    return clientes_db
    
def generar_respaldo_txt():
    """
    Genera un archivo de respaldo con la información de todos los clientes en el mismo directorio del proyecto.
    Sobrescribe cualquier respaldo anterior llamado 'respaldo_clientes.txt'.
    """
    try:
        # Define el nombre de archivo fijo sin timestamp
        nombre_archivo = "respaldo_clientes.txt"
        ruta_archivo = os.path.join(BASE_DIR, nombre_archivo)
        
        # Eliminar el archivo de respaldo anterior si existe
        if os.path.exists(ruta_archivo):
            try:
                os.remove(ruta_archivo)
                print(Fore.YELLOW + f"🗑️  Archivo de respaldo anterior eliminado: {nombre_archivo}" + Style.RESET_ALL)
            except OSError as e:
                print(Fore.RED + f"❌ Error al eliminar el archivo de respaldo anterior {nombre_archivo}: {e}" + Style.RESET_ALL)
                # Si no se puede eliminar el archivo anterior, podría haber un problema de permisos
                # Se podría decidir si continuar y intentar escribir o abortar. 

        # Generar el nuevo respaldo
        clientes = obtener_todos_los_clientes()
        if not clientes:
            print(Fore.YELLOW + "⚠️ No hay clientes para generar el respaldo." + Style.RESET_ALL)
            return

        with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
            archivo.write("\nReporte de Clientes - Estudio Jurídico M&M y Asociados\n")
            archivo.write(f"Fecha de Creación: {datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\n")
            archivo.write("-" * 55 + "\n\n")
            
            for cliente in clientes:
                # Escribe cada cliente en el archivo
                archivo.write(f"ID: {cliente.get('ID', 'N/A')}\n")
                archivo.write(f"Nombre Completo: {cliente.get('Nombre', '')} {cliente.get('Apellido', '')}\n")
                archivo.write(f"Edad: {cliente.get('Edad', 'N/A')}\n")
                archivo.write(f"Email: {cliente.get('Email', '')}\n")
                archivo.write(f"Teléfono: {cliente.get('Telefono', '')}\n")
                archivo.write(f"Fuero: {cliente.get('Fuero', '')}\n")
                archivo.write(f"Tipo de caso: {cliente.get('Tipo_de_caso', '')}\n")
                archivo.write(f"Fecha de registro: {cliente.get('Fecha_registro_formateada', 'N/A')}\n")
                archivo.write("-" * 40 + "\n") # Separador entre clientes

        print(Fore.GREEN + f"✔️  Respaldo creado con éxito en el archivo: {ruta_archivo}" + Style.RESET_ALL)
    
    except Exception as e: # Captura cualquier otra excepción general
        print(Fore.RED + f"❌ Ocurrió un error al generar el respaldo: {e}" + Style.RESET_ALL)


        