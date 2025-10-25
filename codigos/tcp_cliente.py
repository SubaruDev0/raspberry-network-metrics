#!/usr/bin/env python3
import socket
import sys
import select
import csv
import os
import time
from datetime import datetime

# Importar las funciones de métricas
from lab2 import get_network_metrics_filtered

HOST = "127.0.0.1"  # "10.200.210.128" en la U
PORT = 5000

# Configuración para guardar CSV
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_DIR = os.path.join(PROJECT_ROOT, 'registros')
CSV_FILENAME = os.path.join(CSV_DIR, 'metricas_cliente.csv')

# Variables para cálculo de métricas del cliente
start_time = None
total_bytes_received = 0
received_messages = 0


def inicializar_csv_cliente():
    """Crea el archivo CSV del cliente con los headers"""
    os.makedirs(CSV_DIR, exist_ok=True)
    with open(CSV_FILENAME, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'fecha_hora',
            'tam_mensaje_bytes',
            'protocolo',
            'rtt_promedio_ms',
            'rtt_desv_std_ms',
            'jitter_ms',
            'rx_mbps',
            'tx_mbps',
            'gateway',
            'throughput_recepcion_mbps',  # Métrica específica del cliente
            'total_mensajes_recibidos',
            'total_bytes_recibidos'
        ])


def calcular_throughput_recepcion():
    """Calcula el throughput de recepción en Mbps"""
    global start_time, total_bytes_received
    if start_time is None or total_bytes_received == 0:
        return 0.0

    elapsed_time = time.time() - start_time
    if elapsed_time == 0:
        return 0.0

    # Convertir bytes a megabits y dividir por tiempo
    throughput_mbps = (total_bytes_received * 8) / elapsed_time / 1e6
    return throughput_mbps


def guardar_metricas_cliente(tam_mensaje, protocolo="TCP"):
    """Guarda métricas del cliente en el CSV"""
    global received_messages, total_bytes_received

    try:
        # Obtener métricas de red del lab2
        metricas = get_network_metrics_filtered()

        # Calcular throughput específico del cliente
        throughput_recepcion = calcular_throughput_recepcion()

        # Asegurar que el directorio existe
        os.makedirs(CSV_DIR, exist_ok=True)

        with open(CSV_FILENAME, 'a', newline='') as f:
            writer = csv.writer(f)

            # Función helper para manejar valores None
            def safe(v):
                return v if v is not None else 'N/A'

            writer.writerow([
                datetime.now().isoformat(timespec='seconds'),
                tam_mensaje,
                protocolo,
                safe(metricas.get('rtt_avg_ms')),
                safe(metricas.get('rtt_std_ms')),
                safe(metricas.get('jitter_ms')),
                safe(metricas.get('rx_mbps')),
                safe(metricas.get('tx_mbps')),
                safe(metricas.get('gateway')),
                round(throughput_recepcion, 4),  # Throughput de recepción
                received_messages,  # Contador de mensajes
                total_bytes_received  # Total de bytes recibidos
            ])

        return metricas, throughput_recepcion

    except Exception as e:
        print(f"[ERROR] No se pudieron guardar métricas del cliente: {e}")
        return None, 0.0


def main():
    global start_time, total_bytes_received, received_messages

    # Inicializar CSV del cliente
    inicializar_csv_cliente()
    print(f"[INFO] CSV cliente inicializado: {CSV_FILENAME}")

    # Inicializar contadores
    start_time = time.time()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    sock.setblocking(False)  # No bloquea en recv
    print(f"[INFO] Conectado a {HOST}:{PORT}")
    print("Escribe mensajes y presiona Enter (o 'exit' para salir)")
    print("[CLIENT] Esperando mensajes del servidor...")

    try:
        while True:
            read_sockets, _, _ = select.select([sock, sys.stdin], [], [])

            for s in read_sockets:
                if s == sock:
                    try:
                        data = sock.recv(1024)
                        if data:
                            mensaje = data.decode().strip()
                            tam_mensaje = len(data)

                            # Actualizar contadores
                            total_bytes_received += tam_mensaje
                            received_messages += 1

                            # Medir y guardar métricas
                            metricas, throughput = guardar_metricas_cliente(tam_mensaje)

                            print(f"[SRV] {mensaje} | "
                                  f"Tamaño: {tam_mensaje} bytes | "
                                  f"Mensajes: {received_messages} | "
                                  f"Throughput: {throughput:.4f} Mbps | "
                                  f"RTT: {metricas.get('rtt_avg_ms', 'N/A')}ms")

                        else:
                            print("[INFO] Servidor cerró la conexión")
                            return
                    except BlockingIOError:
                        pass

                elif s == sys.stdin:
                    msg = sys.stdin.readline().strip()
                    if msg.lower() == "exit":
                        # Guardar métricas finales antes de salir
                        guardar_metricas_cliente(0)  # Mensaje de 0 bytes indica fin
                        sock.close()
                        print(f"[INFO] Resumen final: {received_messages} mensajes, "
                              f"{total_bytes_received} bytes recibidos")
                        return
                    sock.sendall((msg + "\n").encode())

    except KeyboardInterrupt:
        print(f"\n[INFO] Cliente interrumpido. Resumen: {received_messages} mensajes, "
              f"{total_bytes_received} bytes recibidos")
    except Exception as e:
        print(f"[ERROR] Error en cliente: {e}")
    finally:
        sock.close()
        print(f"[INFO] Cliente desconectado. Datos guardados en: {CSV_FILENAME}")


if __name__ == "__main__":
    main()