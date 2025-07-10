## ESTUDIO JURIDICO M&M y ASOCIADOS

Es un CRUD en Python que tiene como finalidad la gestion de clientes en un Estudio Juridico de La ciudad de La Plata. Creado en el ambito de TalentoTech. El Menu principal esta configurado de la siguinte forma:

1. Agregar cliente
2. Buscar cliente (por ID o Email)
3. Actualizar cliente
4. Eliminar cliente
5. Opciones de Clientes (Requiere contraseña)
6. Buscar por fuero
7. Reporte de historial de acciones
8. Salir

Para la ejeucion del programa el usuario debe ejecutar el modulo main.py

## HERRAMIENTAS, LIBRERIAS USADAS E INSTALADAS

La App esta dividida en modulos y las herrramientas o librerias instaladas son las siguientes:

main.py --> from colorama import Fore, Style.<br>
Colorama es una librería de Python que te permite añadir colores y estilos a la salida de tu consola (terminal)

base_de_datos.py --> import sqlite3, import os, from colorama import Fore Style, import datetime.<br>
SQLite3 es una biblioteca de software que implementa un sistema de gestión de bases de datos relacionales (RDBMS) ligero y basado en archivos. En cuanto a 'os', este módulo permite realizar diversas tareas como manipular archivos y directorios, gestionar procesos y obtener información del sistema. Al importar os, se puede acceder a todas las funciones y constantes que este módulo ofrece. import datetime en código Python, significa que el programa está trayendo la funcionalidad del módulo datetime para poder trabajar con fechas y horas.<br>

utilidades_funciones.py --> from colorama import Fore, Style, init, import re, import os, import datetime.<br>
'init' Esta es una función que se llama al principio del programa. su propósito principal es configurar 'colorama' para que funcione correctamente en tu sistema. En cuanto a 'import re' en un script de Python, significa que el programa está trayendo el módulo re, el cual es la biblioteca incorporada de Python para trabajar con expresiones regulares.


## CONTRASEÑA DE LA OPCION 5 DEL MENU PRINCIPAL

La contraseña de la opcion 5 del Menu principal es: **'1234'**. Una vez dentro se podra acceder a las 'Opciones de Clientes', donde se podra generar un archivo de respalto .txt. A su vez en el mismo submenu la opcion 3 --> se podra generar un reporte filtrando los clientes por edad. 
