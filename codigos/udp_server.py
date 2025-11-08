import socket
import time
import random
import string
import csv
import os
from datetime import datetime

# Importar las funciones de métricas
from lab2 import get_network_metrics_filtered

HOST = "0.0.0.0"
PORT = 5001  # Puerto diferente para UDP

# Tamaño de mensaje variable (para testing: 5-20 caracteres)
MIN_LEN = 5
MAX_LEN = 20

# Intervalo variable entre envíos (segundos)
INTERVAL_MIN = 1
INTERVAL_MAX = 5

# Guardar CSV dentro de la carpeta registros/udp/ en la raíz del proyecto
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_DIR = os.path.join(PROJECT_ROOT, 'registros', 'udp')
CSV_FILENAME = os.path.join(CSV_DIR, 'metricas_servidor.csv')


def random_payload():
    """Genera mensaje aleatorio como pide el PDF"""
    size = random.randint(MIN_LEN, MAX_LEN)
    return ''.join(random.choices(string.ascii_letters + string.digits, k=size))


def inicializar_csv():
    """Crea el archivo CSV con los headers (asegura que exista la carpeta registros/udp)"""
    os.makedirs(CSV_DIR, exist_ok=True)
    with open(CSV_FILENAME, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'fecha_hora', 
            'tam_payload_bytes', 
            'protocolo',
            'mensaje',
            'rtt_promedio_ms', 
            'rtt_desv_std_ms', 
            'jitter_ms',
            'rx_mbps', 
            'tx_mbps', 
            'gateway'
        ])


def guardar_metricas_csv(payload_size, mensaje, protocolo="UDP"):
    """Guarda métricas actuales en el CSV"""
    try:
        # Obtener métricas de red
        metricas = get_network_metrics_filtered()

        # Asegurarnos de que el directorio existe (doble protección)
        os.makedirs(CSV_DIR, exist_ok=True)

        with open(CSV_FILENAME, 'a', newline='') as f:
            writer = csv.writer(f)
            # Convertir None a 'N/A' para evitar celdas vacías en el CSV
            def safe(v):
                return v if v is not None else 'N/A'

            writer.writerow([
                datetime.now().isoformat(timespec='seconds'),
                payload_size,
                protocolo,
                mensaje,
                metricas.get('rtt_avg_ms', 'N/A'),
                metricas.get('rtt_std_ms', 'N/A'),
                metricas.get('jitter_ms', 'N/A'),
                metricas.get('rx_mbps', 'N/A'),
                metricas.get('tx_mbps', 'N/A'),
                metricas.get('gateway', 'N/A')
            ])

        return metricas
    except Exception as e:
        print(f"[ERROR] No se pudieron guardar métricas: {e}")
        return None


def main():
    # Inicializar archivo CSV
    inicializar_csv()
    print(f"[INFO] CSV inicializado: {CSV_FILENAME}")

    # 🔄 CAMBIO TCP→UDP: SOCK_DGRAM en lugar de SOCK_STREAM
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # 🔄 CAMBIO TCP→UDP: bind sin listen (UDP no tiene conexiones)
    server.bind((HOST, PORT))
    print(f"[INFO] Servidor UDP escuchando en {HOST}:{PORT}")

    last_send = time.time()
    next_interval = random.uniform(INTERVAL_MIN, INTERVAL_MAX)
    server.settimeout(0.1)

    # 🔄 CAMBIO TCP→UDP: No hay accept(), guardamos la dirección del primer cliente
    client_addr = None

    try:
        while True:
            now = time.time()
            
            # Enviar carga aleatoria cuando toque (y tengamos un cliente conocido)
            if client_addr and now - last_send >= next_interval:
                payload = random_payload()
                try:
                    # 🔄 CAMBIO TCP→UDP: sendto en lugar de sendall
                    server.sendto((payload + "\n").encode(), client_addr)

                    # MEDIR Y GUARDAR MÉTRICAS (lo que pide el PDF) + el mensaje
                    metricas = guardar_metricas_csv(len(payload), payload)

                    print(f"[SEND] '{payload}' ({len(payload)} bytes) → {client_addr}  "
                          f"RTT: {metricas.get('rtt_avg_ms', 'N/A')}ms  "
                          f"Jitter: {metricas.get('jitter_ms', 'N/A')}ms  "
                          f"Next: {next_interval:.2f}s")

                except Exception as e:
                    print(f"[ERROR] Error enviando a cliente: {e}")

                last_send = now
                next_interval = random.uniform(INTERVAL_MIN, INTERVAL_MAX)

            # Recepción no bloqueante
            try:
                # 🔄 CAMBIO TCP→UDP: recvfrom en lugar de recv
                data, addr = server.recvfrom(1024)
                if data:
                    # Guardar dirección del cliente si es la primera vez
                    if client_addr is None:
                        client_addr = addr
                        print(f"[INFO] Cliente conectado desde: {addr}")
                    
                    # Eco: responder al remitente
                    server.sendto(data, addr)
            except socket.timeout:
                pass

    except KeyboardInterrupt:
        print("\n[INFO] Servidor interrumpido por usuario")
    finally:
        server.close()
        print("[INFO] Servidor UDP detenido.")
        print(f"[INFO] Datos guardados en: {CSV_FILENAME}")


if __name__ == "__main__":
    main()

