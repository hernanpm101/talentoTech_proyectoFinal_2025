# Main principal del CRUD ESTUDIO JURIDICO M&M y ASOCIADOS

from colorama import Fore, Style
from utilidades_funciones import limpiar_pantalla, pedir_numero_entero, registrar_opcion, mostrar_opciones_seleccionadas
import gestor_clientes # Importa el módulo gestor_clientes
import base_de_datos # Importa el módulo de la base de datos

# Contraseña 🔐 para la opción 5 del MENU principal 
PASSWORD_ADMIN = "1234"

# Lista para registrar las opciones seleccionadas por el usuario durante la sesión
opciones_seleccionadas = []

def menu():
    """Función principal que ejecuta el menú interactivo del CRUD."""
    base_de_datos.inicializar_db() # Inicializa la base de datos al inicio
 
    while True:
        limpiar_pantalla()
        print(Fore.BLUE + "\n---- ⚖️  Bienvenidos al Estudio Juridico M&M 📖 ----" + Style.RESET_ALL)  
        print(Fore.BLUE + "\t\t y Asociados." + Style.RESET_ALL) 
        print("1. Agregar cliente") 
        print("2. Buscar cliente (por ID o Email)")
        print("3. Actualizar cliente")
        print("4. Eliminar cliente")
        print("5. Opciones de Clientes (Requiere contraseña)") 
        print("6. Buscar por fuero")
        print("7. Reporte de historial de acciones")
        print("8. Salir")

        opcion_int = pedir_numero_entero(Fore.YELLOW + "Seleccione una opción: " + Style.RESET_ALL,
                                         Fore.RED + "Entrada inválida. Por favor, ingrese un número del 1 al 8." + Style.RESET_ALL)

        match opcion_int:
            case 1:
                gestor_clientes.agregar_cliente(opciones_seleccionadas)
            case 2:
                registrar_opcion("Buscar cliente por ID/Email", opciones_seleccionadas_list=opciones_seleccionadas)
                gestor_clientes.buscar_cliente()
            case 3:
                registrar_opcion("Actualizar cliente", opciones_seleccionadas_list=opciones_seleccionadas)
                gestor_clientes.actualizar_cliente()
            case 4:
                registrar_opcion("Eliminar cliente", opciones_seleccionadas_list=opciones_seleccionadas)
                gestor_clientes.eliminar_cliente()
            case 5:
                # submenú en gestor_clientes
                gestor_clientes.menu_mostrar_clientes(PASSWORD_ADMIN, opciones_seleccionadas)
            case 6:
                registrar_opcion("Buscar por fuero", opciones_seleccionadas_list=opciones_seleccionadas)
                gestor_clientes.buscar_por_fuero()
            case 7:
                registrar_opcion("Mostrar historial de acciones", opciones_seleccionadas_list=opciones_seleccionadas)
                mostrar_opciones_seleccionadas(opciones_seleccionadas)
            case 8:
                print(Fore.CYAN + "\nSaliendo del programa 👋. Gracias por su consulta!" + Style.RESET_ALL)
                print(Fore.CYAN + "Sus datos aportados estan protegidos segun Ley 25.326." + Style.RESET_ALL)
                print(Fore.CYAN + "En breve un miembro de nuestro equipo lo contactara.\n" + Style.RESET_ALL)
                break
            case _:
                print(Fore.RED + "❌ Opción inválida. Por favor, ingrese un número entre 1 y 8." + Style.RESET_ALL)
                input("Presione Enter para continuar...")


if __name__ == "__main__":
    menu()

    