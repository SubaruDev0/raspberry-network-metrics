"""
MENÚ PRINCIPAL - Laboratorio 2 Redes
Sistema Cliente-Servidor con métricas de red
Soporta TCP y UDP
"""

import os
import sys
import subprocess
import time
from pathlib import Path

# Configuración de rutas
PROJECT_ROOT = Path(__file__).parent.parent
CODIGOS_DIR = Path(__file__).parent
REGISTROS_DIR = PROJECT_ROOT / "registros"
GRAFICOS_DIR = PROJECT_ROOT / "graficos"

# Asegurar que existen las carpetas
(REGISTROS_DIR / "tcp").mkdir(parents=True, exist_ok=True)
(REGISTROS_DIR / "udp").mkdir(parents=True, exist_ok=True)
(GRAFICOS_DIR / "tcp" / "cliente").mkdir(parents=True, exist_ok=True)
(GRAFICOS_DIR / "tcp" / "server").mkdir(parents=True, exist_ok=True)
(GRAFICOS_DIR / "udp" / "cliente").mkdir(parents=True, exist_ok=True)
(GRAFICOS_DIR / "udp" / "server").mkdir(parents=True, exist_ok=True)


class Colors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    END = '\033[0m'
    BOLD = '\033[1m'


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(role, protocolo=""):
    clear_screen()
    print(f"{Colors.CYAN}{'=' * 70}{Colors.END}")
    titulo = f"     LABORATORIO 2 - REDES ({role})"
    if protocolo:
        titulo += f" [{protocolo}]"
    print(f"{Colors.BOLD}{Colors.PURPLE}{titulo}{Colors.END}")
    print(f"{Colors.CYAN}{'=' * 70}{Colors.END}")
    print(f"{Colors.BLUE}Sistema Cliente-Servidor con Métricas de Red{Colors.END}")
    print(f"{Colors.YELLOW}Modo: {role}{' - Protocolo: ' + protocolo if protocolo else ''}{Colors.END}")
    print(f"{Colors.CYAN}{'=' * 70}{Colors.END}\n")


def wait_enter():
    input(f"\n{Colors.YELLOW}Presiona Enter para continuar...{Colors.END}")


def run_script(script_name, description):
    """Ejecuta un script de Python"""
    print(f"\n{Colors.BLUE}{description}...{Colors.END}")
    try:
        script_path = CODIGOS_DIR / script_name
        if not script_path.exists():
            print(f"{Colors.RED}❌ No se encuentra {script_name}{Colors.END}")
            return False

        subprocess.run([sys.executable, str(script_path)])
        return True
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}🛑 Ejecución interrumpida{Colors.END}")
        return True
    except Exception as e:
        print(f"{Colors.RED}❌ Error: {e}{Colors.END}")
        return False


def menu_servidor_tcp():
    """Menú específico para el servidor TCP"""
    while True:
        print_header("SERVIDOR", "TCP")
        print(f"{Colors.BOLD}🎯 OPCIONES DEL SERVIDOR TCP:{Colors.END}")
        print(f"{Colors.GREEN}1.{Colors.END} 🚀 Ejecutar Servidor TCP")
        print(f"{Colors.GREEN}2.{Colors.END} 📊 Generar Gráficos del Servidor TCP")
        print(f"{Colors.GREEN}3.{Colors.END} 🔍 Ver métricas de red")
        print(f"{Colors.GREEN}4.{Colors.END} 📁 Explorar archivos del servidor TCP")
        print(f"{Colors.GREEN}0.{Colors.END} 🔙 Volver")
        print(f"{Colors.CYAN}{'-' * 70}{Colors.END}")

        opcion = input(f"\n{Colors.BOLD}Selecciona una opción (0-4): {Colors.END}").strip()

        if opcion == '0':
            break
        elif opcion == '1':
            print(f"{Colors.YELLOW}💡 El servidor TCP estará en 0.0.0.0:5000{Colors.END}")
            print(f"{Colors.YELLOW}💡 Los clientes pueden conectarse a tu IP{Colors.END}")
            run_script("tcp_server.py", "Iniciando Servidor TCP")
            wait_enter()
        elif opcion == '2':
            run_script("graficos_tcp_servidor.py", "Generando gráficos del servidor TCP")
            wait_enter()
        elif opcion == '3':
            run_script("lab2.py", "Medición de métricas de red")
            wait_enter()
        elif opcion == '4':
            explorar_archivos("servidor", "tcp")
        else:
            print(f"{Colors.RED}❌ Opción inválida{Colors.END}")
            time.sleep(1)


def menu_servidor_udp():
    """Menú específico para el servidor UDP"""
    while True:
        print_header("SERVIDOR", "UDP")
        print(f"{Colors.BOLD}🎯 OPCIONES DEL SERVIDOR UDP:{Colors.END}")
        print(f"{Colors.GREEN}1.{Colors.END} 🚀 Ejecutar Servidor UDP")
        print(f"{Colors.GREEN}2.{Colors.END} 📊 Generar Gráficos del Servidor UDP")
        print(f"{Colors.GREEN}3.{Colors.END} 🔍 Ver métricas de red")
        print(f"{Colors.GREEN}4.{Colors.END} 📁 Explorar archivos del servidor UDP")
        print(f"{Colors.GREEN}0.{Colors.END} 🔙 Volver")
        print(f"{Colors.CYAN}{'-' * 70}{Colors.END}")

        opcion = input(f"\n{Colors.BOLD}Selecciona una opción (0-4): {Colors.END}").strip()

        if opcion == '0':
            break
        elif opcion == '1':
            print(f"{Colors.YELLOW}💡 El servidor UDP estará en 0.0.0.0:5001{Colors.END}")
            print(f"{Colors.YELLOW}💡 Los clientes pueden conectarse a tu IP{Colors.END}")
            run_script("udp_server.py", "Iniciando Servidor UDP")
            wait_enter()
        elif opcion == '2':
            run_script("graficos_udp_servidor.py", "Generando gráficos del servidor UDP")
            wait_enter()
        elif opcion == '3':
            run_script("lab2.py", "Medición de métricas de red")
            wait_enter()
        elif opcion == '4':
            explorar_archivos("servidor", "udp")
        else:
            print(f"{Colors.RED}❌ Opción inválida{Colors.END}")
            time.sleep(1)


def menu_cliente_tcp():
    """Menú específico para el cliente TCP"""
    while True:
        print_header("CLIENTE", "TCP")
        print(f"{Colors.BOLD}🎯 OPCIONES DEL CLIENTE TCP:{Colors.END}")
        print(f"{Colors.GREEN}1.{Colors.END} 💻 Ejecutar Cliente TCP")
        print(f"{Colors.GREEN}2.{Colors.END} 📊 Generar Gráficos del Cliente TCP")
        print(f"{Colors.GREEN}3.{Colors.END} 🔍 Ver métricas de red")
        print(f"{Colors.GREEN}4.{Colors.END} 📁 Explorar archivos del cliente TCP")
        print(f"{Colors.GREEN}0.{Colors.END} 🔙 Volver")
        print(f"{Colors.CYAN}{'-' * 70}{Colors.END}")

        opcion = input(f"\n{Colors.BOLD}Selecciona una opción (0-4): {Colors.END}").strip()

        if opcion == '0':
            break
        elif opcion == '1':
            print(f"{Colors.YELLOW}💡 Conectándose al servidor en 127.0.0.1:5000{Colors.END}")
            print(f"{Colors.YELLOW}💡 Cambia la IP en tcp_cliente.py para conectar al servidor real{Colors.END}")
            run_script("tcp_cliente.py", "Iniciando Cliente TCP")
            wait_enter()
        elif opcion == '2':
            run_script("graficos_tcp_cliente.py", "Generando gráficos del cliente TCP")
            wait_enter()
        elif opcion == '3':
            run_script("lab2.py", "Medición de métricas de red")
            wait_enter()
        elif opcion == '4':
            explorar_archivos("cliente", "tcp")
        else:
            print(f"{Colors.RED}❌ Opción inválida{Colors.END}")
            time.sleep(1)


def menu_cliente_udp():
    """Menú específico para el cliente UDP"""
    while True:
        print_header("CLIENTE", "UDP")
        print(f"{Colors.BOLD}🎯 OPCIONES DEL CLIENTE UDP:{Colors.END}")
        print(f"{Colors.GREEN}1.{Colors.END} 💻 Ejecutar Cliente UDP")
        print(f"{Colors.GREEN}2.{Colors.END} 📊 Generar Gráficos del Cliente UDP")
        print(f"{Colors.GREEN}3.{Colors.END} 🔍 Ver métricas de red")
        print(f"{Colors.GREEN}4.{Colors.END} 📁 Explorar archivos del cliente UDP")
        print(f"{Colors.GREEN}0.{Colors.END} 🔙 Volver")
        print(f"{Colors.CYAN}{'-' * 70}{Colors.END}")

        opcion = input(f"\n{Colors.BOLD}Selecciona una opción (0-4): {Colors.END}").strip()

        if opcion == '0':
            break
        elif opcion == '1':
            print(f"{Colors.YELLOW}💡 Conectándose al servidor en 127.0.0.1:5001{Colors.END}")
            print(f"{Colors.YELLOW}💡 Cambia la IP en udp_cliente.py para conectar al servidor real{Colors.END}")
            run_script("udp_cliente.py", "Iniciando Cliente UDP")
            wait_enter()
        elif opcion == '2':
            run_script("graficos_udp_cliente.py", "Generando gráficos del cliente UDP")
            wait_enter()
        elif opcion == '3':
            run_script("lab2.py", "Medición de métricas de red")
            wait_enter()
        elif opcion == '4':
            explorar_archivos("cliente", "udp")
        else:
            print(f"{Colors.RED}❌ Opción inválida{Colors.END}")
            time.sleep(1)


def menu_servidor():
    """Menú que elige protocolo para servidor"""
    while True:
        print_header("SERVIDOR")
        print(f"{Colors.BOLD}🎯 SELECCIONA EL PROTOCOLO:{Colors.END}")
        print(f"{Colors.GREEN}1.{Colors.END} 🔵 TCP (Transmission Control Protocol)")
        print(f"{Colors.GREEN}2.{Colors.END} 🟢 UDP (User Datagram Protocol)")
        print(f"{Colors.GREEN}0.{Colors.END} 🔙 Volver")
        print(f"{Colors.CYAN}{'-' * 70}{Colors.END}")

        opcion = input(f"\n{Colors.BOLD}Selecciona el protocolo (0-2): {Colors.END}").strip()

        if opcion == '0':
            break
        elif opcion == '1':
            menu_servidor_tcp()
        elif opcion == '2':
            menu_servidor_udp()
        else:
            print(f"{Colors.RED}❌ Opción inválida{Colors.END}")
            time.sleep(1)


def menu_cliente():
    """Menú que elige protocolo para cliente"""
    while True:
        print_header("CLIENTE")
        print(f"{Colors.BOLD}🎯 SELECCIONA EL PROTOCOLO:{Colors.END}")
        print(f"{Colors.GREEN}1.{Colors.END} 🔵 TCP (Transmission Control Protocol)")
        print(f"{Colors.GREEN}2.{Colors.END} 🟢 UDP (User Datagram Protocol)")
        print(f"{Colors.GREEN}0.{Colors.END} 🔙 Volver")
        print(f"{Colors.CYAN}{'-' * 70}{Colors.END}")

        opcion = input(f"\n{Colors.BOLD}Selecciona el protocolo (0-2): {Colors.END}").strip()

        if opcion == '0':
            break
        elif opcion == '1':
            menu_cliente_tcp()
        elif opcion == '2':
            menu_cliente_udp()
        else:
            print(f"{Colors.RED}❌ Opción inválida{Colors.END}")
            time.sleep(1)


def explorar_archivos(rol, protocolo):
    """Explora archivos según rol y protocolo"""
    print(f"\n{Colors.BLUE}📁 ARCHIVOS DEL {rol.upper()} {protocolo.upper()}{Colors.END}")
    print(f"{Colors.CYAN}{'-' * 70}{Colors.END}")

    # Archivo CSV correspondiente
    if rol == "servidor":
        csv_file = REGISTROS_DIR / protocolo / "metricas_servidor.csv"
    else:
        csv_file = REGISTROS_DIR / protocolo / "metricas_cliente.csv"

    if csv_file.exists():
        with open(csv_file, 'r') as f:
            lineas = len(f.readlines())
        print(f"{Colors.GREEN}✅ {csv_file.name}: {lineas - 1} registros{Colors.END}")
    else:
        print(f"{Colors.YELLOW}📝 No hay datos del {rol} {protocolo.upper()} aún{Colors.END}")

    # Verificar gráficos
    if rol == "servidor":
        graficos_dir = GRAFICOS_DIR / protocolo / "server"
    else:
        graficos_dir = GRAFICOS_DIR / protocolo / "cliente"

    if graficos_dir.exists():
        png_files = list(graficos_dir.rglob("*.png"))
        if png_files:
            print(f"{Colors.GREEN}📊 Gráficos: {len(png_files)} archivos{Colors.END}")
            for png in png_files:
                print(f"  - {png.name}")
        else:
            print(f"{Colors.YELLOW}📝 No hay gráficos del {rol} {protocolo.upper()}{Colors.END}")
    else:
        print(f"{Colors.YELLOW}📝 No hay carpeta de gráficos del {rol} {protocolo.upper()}{Colors.END}")

    wait_enter()


def main():
    """Menú principal que pregunta si es Cliente o Servidor"""
    while True:
        clear_screen()
        print(f"{Colors.CYAN}{'=' * 70}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.PURPLE}       LABORATORIO 2 - REDES DE COMPUTADORES{Colors.END}")
        print(f"{Colors.CYAN}{'=' * 70}{Colors.END}")
        print(f"{Colors.BLUE}Selecciona el modo de ejecución:{Colors.END}")
        print(f"{Colors.GREEN}1.{Colors.END} 🖥️  MODO SERVIDOR (Raspberry Pi A)")
        print(f"{Colors.GREEN}2.{Colors.END} 💻 MODO CLIENTE (Raspberry Pi B)")
        print(f"{Colors.GREEN}0.{Colors.END} ❌ Salir")
        print(f"{Colors.CYAN}{'-' * 70}{Colors.END}")
        print(f"\n{Colors.YELLOW}📌 Ambos modos soportan TCP y UDP{Colors.END}")

        try:
            opcion = input(f"\n{Colors.BOLD}Selecciona el modo (0-2): {Colors.END}").strip()

            if opcion == '0':
                print(f"\n{Colors.GREEN}👋 ¡Hasta luego!{Colors.END}")
                break
            elif opcion == '1':
                menu_servidor()
            elif opcion == '2':
                menu_cliente()
            else:
                print(f"{Colors.RED}❌ Opción inválida{Colors.END}")
                time.sleep(1)

        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}🛑 Programa interrumpido{Colors.END}")
            break
        except Exception as e:
            print(f"{Colors.RED}❌ Error: {e}{Colors.END}")
            wait_enter()


if __name__ == "__main__":
    main()

