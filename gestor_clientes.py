# Gestor de clientes

from colorama import Fore, Style
# Importa las funciones de utilidades.py
from utilidades_funciones import (
    pedir_entrada_no_vacia, pedir_email_valido, pedir_telefono_valido,
    pedir_numero_entero, validar_email, validar_telefono, registrar_opcion,
    pedir_edad_valida, 
    MAX_LEN_NOMBRE_APELLIDO, MAX_LEN_EMAIL, MAX_LEN_TELEFONO, MAX_LEN_FUERO_TIPO_CASO # Constantes importadas
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
        print(f"Edad: {cliente.get('Edad', 'N/A')}")
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
    print(Fore.BLUE + "\n--- Agregar Nuevo Cliente ---" + Style.RESET_ALL)

    nombre = pedir_entrada_no_vacia("Nombre: ", solo_letras=True, max_len=MAX_LEN_NOMBRE_APELLIDO).capitalize()
    apellido = pedir_entrada_no_vacia("Apellido: ", solo_letras=True, max_len=MAX_LEN_NOMBRE_APELLIDO).capitalize()
    
    # función para validar el rango de edad
    edad = pedir_edad_valida("Edad: ")

    # pedir_email_valido y pedir_telefono_valido ya usan MAX_LEN_EMAIL y MAX_LEN_TELEFONO internamente
    email = pedir_email_valido("Email: ")
    telefono = pedir_telefono_valido("Teléfono: ")

    fuero = seleccionar_fuero()

    tipo_caso = seleccionar_tipo_caso(fuero)

    # Pasa la 'edad' a la función de la base de datos
    nuevo_id = base_de_datos.insertar_cliente(nombre, apellido, edad, email.lower(), telefono, fuero, tipo_caso)

    if nuevo_id is not None:
        print(Fore.GREEN + "✔️  Cliente agregado con éxito con ID: " + str(nuevo_id) + Style.RESET_ALL)
        registrar_opcion(
            "Agregar cliente",
            {
                "ID": nuevo_id,
                "Nombre": nombre,
                "Apellido": apellido,
                "Edad": edad, 
                "Fuero": fuero,
                "Tipo de caso": tipo_caso
            },
            opciones_seleccionadas_list
        )
    else:
        # El mensaje de error específico para email duplicado ya lo imprime base_de_datos.insertar_cliente
        print(Fore.RED + "❌ No se pudo agregar el cliente debido a un error." + Style.RESET_ALL) 

    input("Presione Enter para continuar...")


def buscar_cliente():
    """
    Busca y muestra un cliente por su ID o email.
    Retorna el cliente encontrado o None.
    """
    print(Fore.BLUE + "\n--- Buscar Cliente ---" + Style.RESET_ALL)
    while True:
        criterio = input("¿Desea buscar por ID o Email? (ID/Email): ").strip().lower()
        if criterio == "id":
            cliente_id = pedir_numero_entero("Ingrese el ID del cliente: ", Fore.RED + "ID inválido. Por favor, ingrese un número entero." + Style.RESET_ALL)
            found_client = base_de_datos.obtener_cliente_por_id(cliente_id)
            if found_client:
                print(Fore.GREEN + "\n✔️ Cliente encontrado:" + Style.RESET_ALL)
                mostrar_cliente(found_client)
            else:
                print(Fore.RED + "❌ Cliente no encontrado con ese ID." + Style.RESET_ALL)
            input("Presione Enter para continuar...")
            return found_client

        elif criterio == "email":
            email = pedir_email_valido("Ingrese el email del cliente: ").lower() # Usa la validación de email
            found_client = base_de_datos.obtener_cliente_por_email(email)
            if found_client:
                print(Fore.GREEN + "\n✔️ Cliente encontrado:" + Style.RESET_ALL)
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

        # Nombre
        nombre_input = input(f"Nuevo nombre ({cliente_encontrado['Nombre']}): ").strip()
        if nombre_input: # Solo valida si el usuario ingresó algo
            if not nombre_input.replace(' ', '').isalpha() or len(nombre_input) > MAX_LEN_NOMBRE_APELLIDO:
                print(Fore.RED + f"❌ Nombre inválido. Solo se permiten letras y un máximo de {MAX_LEN_NOMBRE_APELLIDO} caracteres. No se actualizó el nombre." + Style.RESET_ALL)
                nombre = cliente_encontrado['Nombre'] # Revierte al valor original si es inválido
            else:
                nombre = nombre_input.capitalize()
        else:
            nombre = cliente_encontrado['Nombre']

        # Apellido
        apellido_input = input(f"Nuevo apellido ({cliente_encontrado['Apellido']}): ").strip()
        if apellido_input: # Solo valida si el usuario ingresó algo
            if not apellido_input.replace(' ', '').isalpha() or len(apellido_input) > MAX_LEN_NOMBRE_APELLIDO:
                print(Fore.RED + f"❌ Apellido inválido. Solo se permiten letras y un máximo de {MAX_LEN_NOMBRE_APELLIDO} caracteres. No se actualizó el apellido." + Style.RESET_ALL)
                apellido = cliente_encontrado['Apellido']
            else:
                apellido = apellido_input.capitalize()
        else:
            apellido = cliente_encontrado['Apellido']
        
        # Edad (usando pedir_edad_valida si se ingresa un valor)
        edad_input = input(f"Nueva edad ({cliente_encontrado.get('Edad', 'N/A')}): ").strip()
        if edad_input:
            try:
                edad = pedir_edad_valida(f"Edad ({edad_input}): ", min_edad=0, max_edad=120) # Re-valida la entrada
            except ValueError: # pedir_edad_valida ya maneja esto, pero por si acaso.
                print(Fore.RED + "❌ Edad inválida. Debe ser un número. No se actualizó la edad." + Style.RESET_ALL)
                edad = cliente_encontrado.get('Edad')
        else:
            edad = cliente_encontrado.get('Edad')

        # Email (usando pedir_email_valido si se ingresa un valor)
        email_input = input(f"Nuevo email ({cliente_encontrado['Email']}): ").strip()
        if email_input:
            if not validar_email(email_input) or len(email_input) > MAX_LEN_EMAIL:
                print(Fore.RED + "❌ Email inválido o demasiado largo. El email no fue actualizado." + Style.RESET_ALL)
                email = cliente_encontrado['Email'] # Revierte al valor original si es inválido
            else:
                email = email_input.lower() # Siempre guarda en minúsculas
        else:
            email = cliente_encontrado['Email']

        # Teléfono (usando validar_telefono si se ingresa un valor)
        telefono_input = input(f"Nuevo teléfono ({cliente_encontrado['Telefono']}): ").strip()
        if telefono_input:
            if not validar_telefono(telefono_input) or len(telefono_input) > MAX_LEN_TELEFONO:
                print(Fore.RED + "❌ Teléfono inválido o demasiado largo. Solo se permiten dígitos. El teléfono no fue actualizado." + Style.RESET_ALL)
                telefono = cliente_encontrado['Telefono']
            else:
                telefono = telefono_input
        else:
            telefono = cliente_encontrado['Telefono']

        fuero = cliente_encontrado['Fuero']
        tipo_caso = cliente_encontrado['Tipo_de_caso'] # Ojo, nombre de columna

        cambiar_fuero = input("¿Desea cambiar el fuero y tipo de caso? (s/n): ").lower()
        if cambiar_fuero == 's':
            fuero = seleccionar_fuero()
            tipo_caso = seleccionar_tipo_caso(fuero)

        
        if base_de_datos.actualizar_cliente_db(
            cliente_encontrado['ID'], nombre, apellido, edad, email, telefono, fuero, tipo_caso
        ):
            print(Fore.GREEN + f"✔️ Cliente con ID {cliente_encontrado['ID']} actualizado con éxito." + Style.RESET_ALL)
        else:
            # El mensaje de error específico para email duplicado ya lo imprime base_de_datos.actualizar_cliente_db
            print(Fore.RED + "❌ No se pudo actualizar el cliente debido a un error." + Style.RESET_ALL)

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


def buscar_por_fuero():
    """Busca y muestra clientes filtrados por un fuero específico."""
    print(Fore.BLUE + "\n--- Buscar Clientes por Fuero ---" + Style.RESET_ALL)
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

# filtrar clientes por edad
def filtrar_clientes_por_edad():
    """
    Filtra y muestra clientes según si son mayores o menores de edad.
    """
    print(Fore.BLUE + "\n--- Reporte de Clientes por Edad ---" + Style.RESET_ALL)
    mayores_edad = base_de_datos.obtener_clientes_mayores_de_edad()
    menores_edad = base_de_datos.obtener_clientes_menores_de_edad()

    print(Fore.MAGENTA + "\n--- Clientes Mayores de 18 años ---" + Style.RESET_ALL)
    if mayores_edad:
        for cliente in mayores_edad:
            print(Fore.BLUE + f"\n--- Cliente (ID: {cliente.get('ID', 'N/A')}) ---" + Style.RESET_ALL)
            mostrar_cliente(cliente)
    else:
        print(Fore.YELLOW + "No se encontraron clientes mayores de 18 años." + Style.RESET_ALL)
    
    print(Fore.MAGENTA + "\n--- Clientes Menores de 18 años ---" + Style.RESET_ALL)
    if menores_edad:
        for cliente in menores_edad:
            print(Fore.BLUE + f"\n--- Cliente (ID: {cliente.get('ID', 'N/A')}) ---" + Style.RESET_ALL)
            mostrar_cliente(cliente)
    else:
        print(Fore.YELLOW + "No se encontraron clientes menores de 18 años." + Style.RESET_ALL)
    
    print(Fore.MAGENTA + "---------------------------------------" + Style.RESET_ALL)
    input("Presione Enter para continuar...")


def menu_mostrar_clientes(password_admin, opciones_seleccionadas_list):
    """
    Muestra un submenú para ver todos los clientes o generar un respaldo.
    Requiere contraseña para acceder.
    """
    print(Fore.BLUE + "\n--- Opciones de Administración de Clientes ---" + Style.RESET_ALL)
    password_ingresada = input(Fore.YELLOW + "Ingrese la contraseña para acceder: ").strip()
    if password_ingresada != password_admin:
        print(Fore.RED + "❌ Contraseña incorrecta. Acceso denegado." + Style.RESET_ALL)
        input("Presione Enter para continuar...")
        return

    while True:
        print(Fore.BLUE + "\n--- Opciones de Clientes (Administración) ---" + Style.RESET_ALL)
        print("1. Mostrar todos los clientes en pantalla")
        print("2. Generar archivo .txt de clientes (Backup)")
        print("3. Filtrar clientes por edad (Reporte)") #Reporte segun la edad >= a 18 y edad < a 18
        print("4. Volver al menú principal")

        opcion_sub = pedir_numero_entero(Fore.YELLOW + "Seleccione una opción: " + Style.RESET_ALL,
                                         Fore.RED + "Entrada inválida. Por favor, ingrese un número." + Style.RESET_ALL)

        if opcion_sub == 1:
            clientes_db = base_de_datos.obtener_todos_los_clientes()
            if not clientes_db:
                print(Fore.YELLOW + "No hay clientes registrados." + Style.RESET_ALL)
            else:
                print(Fore.MAGENTA + "\n--- Lista de Todos los Clientes ---" + Style.RESET_ALL)
                for i, cliente in enumerate(clientes_db, 1):
                    print(f"\n" + Fore.BLUE + f"Cliente #{i}" + Style.RESET_ALL)
                    mostrar_cliente(cliente)
                print(Fore.MAGENTA + "-----------------------------------" + Style.RESET_ALL)
            input("Presione Enter para continuar...")
            registrar_opcion("Mostrar todos los clientes (con contraseña)", opciones_seleccionadas_list=opciones_seleccionadas_list)
        elif opcion_sub == 2:
            base_de_datos.generar_respaldo_txt()
            input("Presione Enter para continuar...")
            registrar_opcion("Generar respaldo de clientes", opciones_seleccionadas_list=opciones_seleccionadas_list)
        elif opcion_sub == 3:
            filtrar_clientes_por_edad() # Llama a la función de filtrado
            registrar_opcion("Filtrar clientes por edad", opciones_seleccionadas_list=opciones_seleccionadas_list)
        elif opcion_sub == 4:
            print(Fore.CYAN + "Volviendo al menú principal." + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + "❌ Opción inválida. Por favor, ingrese 1, 2, 3 o 4." + Style.RESET_ALL)
            input("Presione Enter para continuar...")