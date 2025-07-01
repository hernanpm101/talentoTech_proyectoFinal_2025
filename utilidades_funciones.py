# Utilidades y Funciones

from colorama import Fore, Style, init
import re
import os
import datetime

init(autoreset=True)

# Constantes para la longitud máxima de las entradas
MAX_LEN_NOMBRE_APELLIDO = 50
MAX_LEN_EMAIL = 255
MAX_LEN_TELEFONO = 20
MAX_LEN_FUERO_TIPO_CASO = 50 

# Funciones de Utilidad Generales

def limpiar_pantalla():
    """Limpia la pantalla de la consola."""
    os.system('cls' if os.name == 'nt' else 'clear')

def validar_email(email):
    """Valida si el formato del email es correcto."""
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(patron, email) is not None

def validar_telefono(telefono):
    """Valida si la cadena del teléfono contiene solo dígitos."""
    return telefono.isdigit()

# Funciones de Utilidad para la Gestión de Errores y Excepciones

def pedir_entrada_no_vacia(mensaje, mensaje_error=" ❌ Este campo no puede estar vacío. Intente de nuevo.", solo_letras=False, max_len=255):
    """
    Pide al usuario una entrada de texto y asegura que no esté vacía.
    Si solo_letras es True, valida que la entrada contenga solo caracteres alfabéticos.
    Asegura que la longitud de la entrada no exceda max_len.
    Reintenta hasta obtener una entrada válida.
    """
    while True:
        valor = input(mensaje).strip()
        if not valor:
            print(Fore.RED + mensaje_error + Style.RESET_ALL)
            continue
        
        # Validación de longitud máxima
        if len(valor) > max_len:
            print(Fore.RED + f"❌ Entrada demasiado larga. Máximo {max_len} caracteres." + Style.RESET_ALL)
            continue

        if solo_letras and not valor.replace(' ', '').isalpha():
            print(Fore.RED + "❌ Entrada inválida. Solo se permiten letras." + Style.RESET_ALL)
            continue
        return valor

def pedir_email_valido(mensaje):
    """
    Pide al usuario un email y lo valida con la función validar_email y la longitud máxima.
    Reintenta hasta obtener un email válido.
    """
    while True:
        email = input(mensaje).strip()
        if len(email) > MAX_LEN_EMAIL: # Validación de longitud para el email
            print(Fore.RED + f"❌ Email demasiado largo. Máximo {MAX_LEN_EMAIL} caracteres." + Style.RESET_ALL)
            continue
        if validar_email(email):
            return email
        else:
            print(Fore.RED + "❌ Email inválido. Por favor, ingrese un email con formato correcto." + Style.RESET_ALL)

def pedir_telefono_valido(mensaje):
    """
    Pide al usuario un número de teléfono y lo valida con la función validar_telefono y la longitud máxima.
    Reintenta hasta obtener un teléfono válido.
    """
    while True:
        telefono = input(mensaje).strip()
        if len(telefono) > MAX_LEN_TELEFONO: # Validación de longitud para el teléfono
            print(Fore.RED + f"❌ Teléfono demasiado largo. Máximo {MAX_LEN_TELEFONO} dígitos." + Style.RESET_ALL)
            continue
        if validar_telefono(telefono):
            return telefono
        else:
            print(Fore.RED + "❌ Teléfono inválido. Solo se permiten dígitos. Intente de nuevo." + Style.RESET_ALL)

def pedir_numero_entero(mensaje, mensaje_error="Entrada inválida. Por favor, ingrese un número entero."):
    """
    Pide al usuario un número entero y lo valida.
    Reintenta hasta obtener una entrada válida.
    """
    while True:
        try:
            valor = input(mensaje).strip()
            return int(valor)
        except ValueError:
            print(Fore.RED + mensaje_error + Style.RESET_ALL)

def pedir_edad_valida(mensaje, min_edad=0, max_edad=120):
    """
    Pide al usuario una edad y valida que sea un número entero dentro de un rango razonable.
    """
    while True:
        edad = pedir_numero_entero(mensaje)
        if min_edad <= edad <= max_edad:
            return edad
        else:
            print(Fore.RED + f"❌ Edad inválida. Debe estar entre {min_edad} y {max_edad}." + Style.RESET_ALL)

def registrar_opcion(opcion_texto, datos_adicionales=None, opciones_seleccionadas_list=None):
    """
    Registra la opción del menú seleccionada por el usuario,
    opcionalmente con datos adicionales y una marca de tiempo.
    Requiere pasar la lista de opciones_seleccionadas explícitamente.
    """
    if opciones_seleccionadas_list is None:
        print(Fore.RED + "Error: La lista de opciones_seleccionadas no fue proporcionada a registrar_opcion." + Style.RESET_ALL)
        return

    timestamp = datetime.datetime.now().isoformat()
    registro = {
        "accion": opcion_texto,
        "timestamp": timestamp
    }
    if datos_adicionales:
        registro["datos"] = datos_adicionales
    opciones_seleccionadas_list.append(registro)

def mostrar_opciones_seleccionadas(opciones_seleccionadas_list):
    """
    Muestra el historial de las opciones del menú seleccionadas por el usuario,
    incluyendo detalles adicionales y la marca de tiempo.
    """
    if not opciones_seleccionadas_list:
        print(Fore.YELLOW + "\n ❌ No se ha seleccionado ninguna opción todavía en esta sesión." + Style.RESET_ALL)
    else:
        print(Fore.MAGENTA + "\n--- Historial Opciones Seleccionadas📝 ---" + Style.RESET_ALL)
        for i, registro in enumerate(opciones_seleccionadas_list, 1):
            accion = registro["accion"]
            datos = registro.get("datos")
            timestamp = registro.get("timestamp", "Fecha/Hora no disponible")

            try:
                dt_object = datetime.datetime.fromisoformat(timestamp)
                timestamp_formateado = dt_object.strftime("%d-%m-%Y %H:%M:%S") #fecha formato usado por mi
            except ValueError:
                timestamp_formateado = timestamp

            if accion == "Agregar cliente" and datos:
                print(f"{i}. " + Fore.GREEN + f"{accion}:" + Style.RESET_ALL)
                print(f"   - ID: {datos.get('ID', 'N/A')}")
                print(f"   - Cliente: {datos.get('Nombre', '')} {datos.get('Apellido', '')}")
                print(f"   - Edad: {datos.get('Edad', 'N/A')}") # Agregado al historial
                print(f"   - Fuero: {datos.get('Fuero', '')}")
                print(f"   - Tipo de caso: {datos.get('Tipo de caso', '')}")
                print(f"   - Fecha: {timestamp_formateado}")
            else:
                print(f"{i}. {accion} (Fecha: {timestamp_formateado})")
        print(Fore.MAGENTA + "------------------------------------------" + Style.RESET_ALL)
    input("Presione Enter para continuar...")