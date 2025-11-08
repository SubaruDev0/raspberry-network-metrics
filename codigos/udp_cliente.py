import sys
import socket
import select
import csv
import os
import time
from datetime import datetime

# Importar las funciones de métricas
from lab2 import get_network_metrics_filtered

HOST = "10.200.210.116"  # "10.200.210.128" en la U
PORT = 5001  # Puerto diferente para UDP

# Configuración para guardar CSV (ahora en carpeta udp/)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_DIR = os.path.join(PROJECT_ROOT, 'registros', 'udp')
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
            'mensaje',
            'rtt_promedio_ms',
            'rtt_desv_std_ms',
            'jitter_ms',
            'rx_mbps',
            'tx_mbps',
            'gateway',
            'throughput_recepcion_mbps',
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


def guardar_metricas_cliente(tam_mensaje, mensaje, protocolo="UDP"):
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
                mensaje,
                safe(metricas.get('rtt_avg_ms')),
                safe(metricas.get('rtt_std_ms')),
                safe(metricas.get('jitter_ms')),
                safe(metricas.get('rx_mbps')),
                safe(metricas.get('tx_mbps')),
                safe(metricas.get('gateway')),
                round(throughput_recepcion, 4),
                received_messages,
                total_bytes_received
            ])

        return metricas, throughput_recepcion

    except Exception as e:
        print(f"[ERROR] No se pudieron guardar métricas del cliente: {e}")
        return None, 0.0


def main():
    global start_time, total_bytes_received, received_messages

    # Inicializar CSV del cliente
    inicializar_csv_cliente()
    print(f"[INFO] CSV cliente UDP inicializado: {CSV_FILENAME}")

    # Inicializar contadores
    start_time = time.time()

    # -------------------------------------------------------------------------
    # NOTA DE SIMILITUD: Este cliente UDP está diseñado para ser lo más similar
    # posible a `tcp_cliente.py`. Las únicas diferencias concretas están marcadas
    # con el prefijo "🔄 CAMBIO TCP↔UDP:" y consisten en:
    #   - UDP utiliza SOCK_DGRAM, sendto(), recvfrom(), sin connect/accept
    #   - TCP utiliza SOCK_STREAM, connect(), sendall(), recv()
    # La lógica de métricas, CSV y manejo de mensajes es idéntica para facilitar
    # comparaciones y evitar divergencias entre versiones.
    # -------------------------------------------------------------------------

    # 🔄 CAMBIO TCP↔UDP: creación del socket (UDP usa SOCK_DGRAM)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 🔄 CAMBIO TCP↔UDP: No hay connect() en UDP, bind a puerto local
    sock.bind(('', 0))  # Bind a puerto aleatorio local
    sock.setblocking(False)  # No bloquea en recvfrom

    server_addr = (HOST, PORT)
    print(f"[INFO] Cliente UDP configurado para comunicarse con {HOST}:{PORT}")

    # 🔄 MEJORA: enviar un mensaje inicial para "registrar" la dirección del cliente
    # en el servidor UDP. Sin esto, el servidor no conoce la dirección del cliente y
    # no enviará payloads proactivos. Este mensaje no requiere interacción del usuario.
    try:
        sock.sendto(("__INIT__\n").encode(), server_addr)
        # Nota: el servidor responderá con eco y/o almacenará la dirección del cliente.
        print(f"[DEBUG] Mensaje inicial enviado al servidor UDP {server_addr}")
    except Exception as e:
        print(f"[WARN] No se pudo enviar mensaje inicial al servidor UDP: {e}")

    print("Escribe mensajes y presiona Enter (o 'exit' para salir)")
    print("[CLIENT] Esperando mensajes del servidor...")

    try:
        while True:
            read_sockets, _, _ = select.select([sock, sys.stdin], [], [])

            for s in read_sockets:
                if s == sock:
                    try:
                        # 🔄 CAMBIO TCP→UDP: recvfrom en lugar de recv
                        data, addr = sock.recvfrom(1024)
                        if data:
                            mensaje = data.decode().strip()
                            tam_mensaje = len(data)

                            # Actualizar contadores
                            total_bytes_received += tam_mensaje
                            received_messages += 1

                            # Medir y guardar métricas (con el mensaje)
                            metricas, throughput = guardar_metricas_cliente(tam_mensaje, mensaje)

                            print(f"[SRV] {mensaje}  "
                                  f"Tamaño: {tam_mensaje} bytes  "
                                  f"Mensajes: {received_messages}  "
                                  f"Throughput: {throughput:.4f} Mbps  "
                                  f"RTT: {metricas.get('rtt_avg_ms', 'N/A')}ms")
                    except BlockingIOError:
                        pass

                elif s == sys.stdin:
                    msg = sys.stdin.readline().strip()
                    if msg.lower() == "exit":
                        sock.close()
                        print(f"[INFO] Resumen final: {received_messages} mensajes, "
                              f"{total_bytes_received} bytes recibidos")
                        return
                    # 🔄 CAMBIO TCP→UDP: sendto en lugar de sendall
                    sock.sendto((msg + "\n").encode(), server_addr)

    except KeyboardInterrupt:
        print(f"\n[INFO] Cliente interrumpido. Resumen: {received_messages} mensajes, "
              f"{total_bytes_received} bytes recibidos")
    except Exception as e:
        print(f"[ERROR] Error en cliente UDP: {e}")
    finally:
        sock.close()
        print(f"[INFO] Cliente UDP desconectado. Datos guardados en: {CSV_FILENAME}")


if __name__ == "__main__":
    main()
