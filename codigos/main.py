#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MENÚ PRINCIPAL - Laboratorio 2 Redes
Versión separada para Cliente y Servidor en diferentes Raspberry Pi
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
REGISTROS_DIR.mkdir(exist_ok=True)
GRAFICOS_DIR.mkdir(exist_ok=True)


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


def print_header(role):
    clear_screen()
    print(f"{Colors.CYAN}{'=' * 60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.PURPLE}     LABORATORIO 2 - REDES ({role}){Colors.END}")
    print(f"{Colors.CYAN}{'=' * 60}{Colors.END}")
    print(f"{Colors.BLUE}Sistema Cliente-Servidor con Métricas de Red{Colors.END}")
    print(f"{Colors.YELLOW}Ejecutando en modo: {role}{Colors.END}")
    print(f"{Colors.CYAN}{'=' * 60}{Colors.END}\n")


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


def menu_servidor():
    """Menú específico para el servidor"""
    while True:
        print_header("SERVIDOR")
        print(f"{Colors.BOLD}🎯 OPCIONES DEL SERVIDOR:{Colors.END}")
        print(f"{Colors.GREEN}1.{Colors.END} 🚀 Ejecutar Servidor TCP")
        print(f"{Colors.GREEN}2.{Colors.END} 📊 Generar Gráficos del Servidor")
        print(f"{Colors.GREEN}3.{Colors.END} 🔍 Ver métricas de red")
        print(f"{Colors.GREEN}4.{Colors.END} 📁 Explorar archivos del servidor")
        print(f"{Colors.GREEN}0.{Colors.END} 🔙 Volver")
        print(f"{Colors.CYAN}{'-' * 60}{Colors.END}")

        opcion = input(f"\n{Colors.BOLD}Selecciona una opción (0-4): {Colors.END}").strip()

        if opcion == '0':
            break
        elif opcion == '1':
            print(f"{Colors.YELLOW}💡 El servidor estará en 0.0.0.0:5000{Colors.END}")
            print(f"{Colors.YELLOW}💡 Los clientes pueden conectarse a tu IP{Colors.END}")
            run_script("tcp_server.py", "Iniciando Servidor TCP")
            wait_enter()
        elif opcion == '2':
            run_script("graficos_servidor.py", "Generando gráficos del servidor")
            wait_enter()
        elif opcion == '3':
            run_script("lab2.py", "Medición de métricas de red")
            wait_enter()
        elif opcion == '4':
            explorar_archivos_servidor()
        else:
            print(f"{Colors.RED}❌ Opción inválida{Colors.END}")
            time.sleep(1)


def menu_cliente():
    """Menú específico para el cliente"""
    while True:
        print_header("CLIENTE")
        print(f"{Colors.BOLD}🎯 OPCIONES DEL CLIENTE:{Colors.END}")
        print(f"{Colors.GREEN}1.{Colors.END} 💻 Ejecutar Cliente TCP")
        print(f"{Colors.GREEN}2.{Colors.END} 📊 Generar Gráficos del Cliente")
        print(f"{Colors.GREEN}3.{Colors.END} 🔍 Ver métricas de red")
        print(f"{Colors.GREEN}4.{Colors.END} 📁 Explorar archivos del cliente")
        print(f"{Colors.GREEN}0.{Colors.END} 🔙 Volver")
        print(f"{Colors.CYAN}{'-' * 60}{Colors.END}")

        opcion = input(f"\n{Colors.BOLD}Selecciona una opción (0-4): {Colors.END}").strip()

        if opcion == '0':
            break
        elif opcion == '1':
            print(f"{Colors.YELLOW}💡 Conectándose al servidor en 127.0.0.1:5000{Colors.END}")
            print(f"{Colors.YELLOW}💡 Cambia la IP en tcp_cliente.py para conectar al servidor real{Colors.END}")
            run_script("tcp_cliente.py", "Iniciando Cliente TCP")
            wait_enter()
        elif opcion == '2':
            run_script("graficos_cliente.py", "Generando gráficos del cliente")
            wait_enter()
        elif opcion == '3':
            run_script("lab2.py", "Medición de métricas de red")
            wait_enter()
        elif opcion == '4':
            explorar_archivos_cliente()
        else:
            print(f"{Colors.RED}❌ Opción inválida{Colors.END}")
            time.sleep(1)


def explorar_archivos_servidor():
    """Explora archivos del servidor"""
    print(f"\n{Colors.BLUE}📁 ARCHIVOS DEL SERVIDOR{Colors.END}")
    print(f"{Colors.CYAN}{'-' * 50}{Colors.END}")

    servidor_csv = REGISTROS_DIR / "metricas_servidor.csv"
    if servidor_csv.exists():
        with open(servidor_csv, 'r') as f:
            lineas = len(f.readlines())
        print(f"{Colors.GREEN}✅ metricas_servidor.csv: {lineas - 1} registros{Colors.END}")
    else:
        print(f"{Colors.YELLOW}📝 No hay datos del servidor aún{Colors.END}")

    # Verificar gráficos del servidor
    graficos_server = GRAFICOS_DIR / "server"
    if graficos_server.exists():
        png_files = list(graficos_server.rglob("*.png"))
        if png_files:
            print(f"{Colors.GREEN}📊 Gráficos del servidor: {len(png_files)} archivos{Colors.END}")
        else:
            print(f"{Colors.YELLOW}📝 No hay gráficos del servidor{Colors.END}")
    else:
        print(f"{Colors.YELLOW}📝 No hay carpeta de gráficos del servidor{Colors.END}")

    wait_enter()


def explorar_archivos_cliente():
    """Explora archivos del cliente"""
    print(f"\n{Colors.BLUE}📁 ARCHIVOS DEL CLIENTE{Colors.END}")
    print(f"{Colors.CYAN}{'-' * 50}{Colors.END}")

    cliente_csv = REGISTROS_DIR / "metricas_cliente.csv"
    if cliente_csv.exists():
        with open(cliente_csv, 'r') as f:
            lineas = len(f.readlines())
        print(f"{Colors.GREEN}✅ metricas_cliente.csv: {lineas - 1} registros{Colors.END}")
    else:
        print(f"{Colors.YELLOW}📝 No hay datos del cliente aún{Colors.END}")

    # Verificar gráficos del cliente
    graficos_cliente_dir = GRAFICOS_DIR / "cliente"
    if graficos_cliente_dir.exists():
        png_files = list(graficos_cliente_dir.rglob("*.png"))
        if png_files:
            print(f"{Colors.GREEN}📊 Gráficos del cliente: {len(png_files)} archivos{Colors.END}")
        else:
            print(f"{Colors.YELLOW}📝 No hay gráficos del cliente{Colors.END}")
    else:
        print(f"{Colors.YELLOW}📝 No hay carpeta de gráficos del cliente{Colors.END}")

    wait_enter()


def main():
    """Menú principal que pregunta si es Cliente o Servidor"""
    while True:
        clear_screen()
        print(f"{Colors.CYAN}{'=' * 60}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.PURPLE}       LABORATORIO 2 - REDES DE COMPUTADORES{Colors.END}")
        print(f"{Colors.CYAN}{'=' * 60}{Colors.END}")
        print(f"{Colors.BLUE}Selecciona el modo de ejecución:{Colors.END}")
        print(f"{Colors.GREEN}1.{Colors.END} 🖥️  MODO SERVIDOR (Raspberry Pi A)")
        print(f"{Colors.GREEN}2.{Colors.END} 💻 MODO CLIENTE (Raspberry Pi B)")
        print(f"{Colors.GREEN}0.{Colors.END} ❌ Salir")
        print(f"{Colors.CYAN}{'-' * 60}{Colors.END}")

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