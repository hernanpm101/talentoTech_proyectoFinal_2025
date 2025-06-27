# Gestor de clientes

from colorama import Fore, Style
# Importa las funciones de utilidades.py
from utilidades_funciones import (
    pedir_entrada_no_vacia, pedir_email_valido, pedir_telefono_valido,
    pedir_numero_entero, validar_email, validar_telefono, registrar_opcion
)
import base_de_datos # Importa módulo de la base de datos

# Fueros
tipos_por_fuero = {
    "Penal": ["Homicidio", "Robo", "Narcotráfico"],
    "Civil": ["Divorcio", "Sucesiones", "Reclamos"],
    "Laboral": ["Despido", "Accidente de trabajo", "Reclamo salarial"],
    "Familia": ["Adopciones", "Tenencia", "Violencia familiar"]
}

def mostrar_cliente(cliente):
    """Imprime los detalles de un cliente de forma legible."""
    
    if isinstance(cliente, dict):
        print(f"ID: {cliente.get('ID', 'N/A')}")
        print(f"Nombre: {cliente.get('Nombre', '')}")
        print(f"Apellido: {cliente.get('Apellido', '')}")
        print(f"Email: {cliente.get('Email', '')}")
        print(f"Telefono: {cliente.get('Telefono', '')}")
        print(f"Fuero: {cliente.get('Fuero', '')}")
        print(f"Tipo de caso: {cliente.get('Tipo_de_caso', '')}")
        print(f"Fecha de registro: {cliente.get('Fecha_registro_formateada', 'N/A')}")
    else:
        print(Fore.RED + "Error: Formato de cliente inválido." + Style.RESET_ALL)


def seleccionar_fuero():
    """Permite al usuario seleccionar un fuero de la lista disponible."""
    while True:
        print("\n" + Fore.CYAN + "Fueros disponibles:" + Style.RESET_ALL)
        for idx, fuero in enumerate(tipos_por_fuero.keys(), start=1):
            print(f"{idx}. {fuero}")

        opcion_str = input("Seleccione el número del Fuero: ").strip()
        if opcion_str.isdigit():
            opcion = int(opcion_str)
            if 1 <= opcion <= len(tipos_por_fuero):
                return list(tipos_por_fuero.keys())[opcion - 1]
            else:
                print(Fore.RED + "❌ Opción inválida. El número no corresponde a un fuero disponible." + Style.RESET_ALL)
        else:
            print(Fore.RED + "❌ Entrada inválida. Por favor, ingrese un número." + Style.RESET_ALL)

def seleccionar_tipo_caso(fuero):
    """Permite al usuario seleccionar un tipo de caso basado en el fuero elegido."""
    tipos = tipos_por_fuero[fuero]
    while True:
        print("\n" + Fore.CYAN + "Tipos de caso disponibles:" + Style.RESET_ALL)
        for idx, tipo in enumerate(tipos, start=1):
            print(f"{idx}. {tipo}")

        opcion_str = input("Seleccione el número del tipo de caso: ").strip()
        if opcion_str.isdigit():
            opcion = int(opcion_str)
            if 1 <= opcion <= len(tipos):
                return tipos[opcion - 1]
            else:
                print(Fore.RED + "❌ Opción inválida. El número no corresponde a un tipo de caso disponible." + Style.RESET_ALL)
        else:
            print(Fore.RED + "❌ Entrada inválida. Por favor, ingrese un número." + Style.RESET_ALL)


def agregar_cliente(opciones_seleccionadas_list):
    """Permite al usuario agregar un nuevo cliente al sistema."""

    nombre = pedir_entrada_no_vacia("Nombre: ", solo_letras=True).capitalize()
    apellido = pedir_entrada_no_vacia("Apellido: ", solo_letras=True).capitalize()

    email = pedir_email_valido("Email: ")
    telefono = pedir_telefono_valido("Teléfono: ")

    fuero = seleccionar_fuero()
    tipo_caso = seleccionar_tipo_caso(fuero)

    nuevo_id = base_de_datos.insertar_cliente(nombre, apellido, email.lower(), telefono, fuero, tipo_caso)

    if nuevo_id is not None:
        print(Fore.GREEN + "✔️  Cliente agregado con éxito con ID: " + str(nuevo_id) + Style.RESET_ALL)
        registrar_opcion(
            "Agregar cliente",
            {
                "ID": nuevo_id,
                "Nombre": nombre,
                "Apellido": apellido,
                "Fuero": fuero,
                "Tipo de caso": tipo_caso
            },
            opciones_seleccionadas_list
        )
    else:
        print(Fore.RED + "❌ No se pudo agregar el cliente." + Style.RESET_ALL) # Mensaje de error si el email ya existe

    input("Presione Enter para continuar...")


def buscar_cliente():
    """
    Busca y muestra un cliente por su ID o email.
    Retorna el cliente encontrado o None.
    """
    while True:
        criterio = input("¿Desea buscar por ID o Email? (ID/Email): ").strip().lower()
        if criterio == "id":
            cliente_id = pedir_numero_entero("Ingrese el ID del cliente: ", Fore.RED + "ID inválido. Por favor, ingrese un número entero." + Style.RESET_ALL)
            found_client = base_de_datos.obtener_cliente_por_id(cliente_id)
            if found_client:
                mostrar_cliente(found_client)
            else:
                print(Fore.RED + "❌ Cliente no encontrado con ese ID." + Style.RESET_ALL)
            input("Presione Enter para continuar...")
            return found_client

        elif criterio == "email":
            email = input("Ingrese el email del cliente: ").strip().lower()
            found_client = base_de_datos.obtener_cliente_por_email(email)
            if found_client:
                mostrar_cliente(found_client)
            else:
                print(Fore.RED + "❌ Cliente no encontrado con ese email." + Style.RESET_ALL)
            input("Presione Enter para continuar...")
            return found_client
        else:
            print(Fore.RED + "❌ Criterio de búsqueda inválido. Por favor, elija 'ID' o 'Email'." + Style.RESET_ALL)


def actualizar_cliente():
    """Permite al usuario actualizar la información de un cliente existente."""
    print(Fore.CYAN + "⚠️  Para actualizar un cliente, primero debe encontrarlo." + Style.RESET_ALL)
    cliente_encontrado = buscar_cliente()

    if cliente_encontrado:
        print(Fore.YELLOW + "\nDeje en blanco los campos que no desea actualizar." + Style.RESET_ALL)

        # valores actuales como valores predeterminados para la entrada
        nombre = input(f"Nuevo nombre ({cliente_encontrado['Nombre']}): ").strip() or cliente_encontrado['Nombre']
        if nombre != cliente_encontrado['Nombre'] and not nombre.replace(' ', '').isalpha():
            print(Fore.RED + "❌ Nombre inválido. Solo se permiten letras. El nombre no fue actualizado." + Style.RESET_ALL)
            nombre = cliente_encontrado['Nombre'] # Revierte al valor original si es inválido
        else:
            nombre = nombre.capitalize()

        apellido = input(f"Nuevo apellido ({cliente_encontrado['Apellido']}): ").strip() or cliente_encontrado['Apellido']
        if apellido != cliente_encontrado['Apellido'] and not apellido.replace(' ', '').isalpha():
            print(Fore.RED + "❌ Apellido inválido. Solo se permiten letras. El apellido no fue actualizado." + Style.RESET_ALL)
            apellido = cliente_encontrado['Apellido']
        else:
            apellido = apellido.capitalize()

        email = input(f"Nuevo email ({cliente_encontrado['Email']}): ").strip() or cliente_encontrado['Email']
        if email != cliente_encontrado['Email'] and not validar_email(email):
            print(Fore.RED + "❌ Email inválido. El email no fue actualizado." + Style.RESET_ALL)
            email = cliente_encontrado['Email'] # Revierte al valor original si es inválido
        email = email.lower() # Siempre guarda en minúsculas

        telefono = input(f"Nuevo teléfono ({cliente_encontrado['Telefono']}): ").strip() or cliente_encontrado['Telefono']
        if telefono != cliente_encontrado['Telefono'] and not validar_telefono(telefono):
            print(Fore.RED + "❌ Teléfono inválido. Solo se permiten dígitos. El teléfono no fue actualizado." + Style.RESET_ALL)
            telefono = cliente_encontrado['Telefono']


        fuero = cliente_encontrado['Fuero']
        tipo_caso = cliente_encontrado['Tipo_de_caso'] # Ojo, nombre de columna

        cambiar_fuero = input("¿Desea cambiar el fuero y tipo de caso? (s/n): ").lower()
        if cambiar_fuero == 's':
            fuero = seleccionar_fuero()
            tipo_caso = seleccionar_tipo_caso(fuero)

        # Llama a la función de la base de datos para actualizar
        if base_de_datos.actualizar_cliente_db(
            cliente_encontrado['ID'], nombre, apellido, email, telefono, fuero, tipo_caso
        ):
            print(Fore.GREEN + f"✔️ Cliente con ID {cliente_encontrado['ID']} actualizado con éxito." + Style.RESET_ALL)
        else:
            print(Fore.RED + "❌ No se pudo actualizar el cliente (posiblemente email duplicado)." + Style.RESET_ALL)

    input("Presione Enter para continuar...")


def eliminar_cliente():
    """Permite al usuario eliminar un cliente del sistema."""
    print(Fore.CYAN + "⚠️  Para eliminar un cliente, primero debe encontrarlo." + Style.RESET_ALL)
    cliente_a_eliminar = buscar_cliente()

    if cliente_a_eliminar:
        confirmar = input(Fore.RED + f"¿Está seguro de eliminar al cliente {cliente_a_eliminar['Nombre']} {cliente_a_eliminar['Apellido']} (ID: {cliente_a_eliminar['ID']})? (s/n): " + Style.RESET_ALL).lower()
        if confirmar == 's':
            if base_de_datos.eliminar_cliente_db(cliente_a_eliminar['ID']):
                print(Fore.GREEN + "✔️ Cliente eliminado con éxito." + Style.RESET_ALL)
            else:
                print(Fore.RED + "❌ No se pudo eliminar el cliente." + Style.RESET_ALL)
        else:
            print(Fore.BLUE + "Eliminación cancelada." + Style.RESET_ALL)
    input("Presione Enter para continuar...")


def mostrar_todos_clientes(password_admin):
    """Muestra la información de todos los clientes registrados, previa validación de contraseña."""
    password_ingresada = input(Fore.YELLOW + "Ingrese la contraseña para ver todos los clientes: ").strip()
    if password_ingresada == password_admin:
        clientes_db = base_de_datos.obtener_todos_los_clientes()
        if not clientes_db:
            print(Fore.YELLOW + "No hay clientes registrados." + Style.RESET_ALL)
        else:
            print(Fore.MAGENTA + "\n--- Lista de Todos los Clientes ---" + Style.RESET_ALL)
            for i, cliente in enumerate(clientes_db, 1):
                # Usamos mostrar_cliente para imprimir los detalles de cada cliente
                # Esto incluye la fecha de registro que se añade en la función
                print(f"\n" + Fore.BLUE + f"Cliente #{i}" + Style.RESET_ALL)
                mostrar_cliente(cliente)
            print(Fore.MAGENTA + "-----------------------------------" + Style.RESET_ALL)
    else:
        print(Fore.RED + "❌ Contraseña incorrecta. Acceso denegado." + Style.RESET_ALL)
    input("Presione Enter para continuar...")


def buscar_por_fuero():
    """Busca y muestra clientes filtrados por un fuero específico."""
    fuero_buscado = seleccionar_fuero()
    encontrados = base_de_datos.buscar_clientes_por_fuero(fuero_buscado)
    if encontrados:
        print(Fore.MAGENTA + f"\n--- Clientes en el fuero de {fuero_buscado} ---" + Style.RESET_ALL)
        for cliente in encontrados:
            print(Fore.BLUE + f"\n--- Cliente (ID: {cliente.get('ID', 'N/A')}) ---" + Style.RESET_ALL)
            mostrar_cliente(cliente)
        print(Fore.MAGENTA + "---------------------------------------" + Style.RESET_ALL)
    else:
        print(Fore.YELLOW + f" ❌ No se encontraron clientes en el fuero de {fuero_buscado}." + Style.RESET_ALL)
    input("Presione Enter para continuar...")