import socket
import time
import random
import string
import csv
import os
from datetime import datetime

# Importar las funciones de métricas (asegúrate de que lab2.py esté en el mismo directorio)
from lab2 import get_network_metrics_filtered

HOST = "0.0.0.0"
PORT = 5000

# Tamaño de mensaje variable (para testing: 5-20 caracteres)
MIN_LEN = 5
MAX_LEN = 20

# Intervalo variable entre envíos (segundos)
INTERVAL_MIN = 1
INTERVAL_MAX = 5

# Guardar CSV dentro de la carpeta registros/tcp/ en la raíz del proyecto
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_DIR = os.path.join(PROJECT_ROOT, 'registros', 'tcp')
CSV_FILENAME = os.path.join(CSV_DIR, 'metricas_servidor.csv')


def random_payload():
    """Genera mensaje aleatorio como pide el PDF"""
    size = random.randint(MIN_LEN, MAX_LEN)
    return ''.join(random.choices(string.ascii_letters + string.digits, k=size))


def inicializar_csv():
    """Crea el archivo CSV con los headers (asegura que exista la carpeta registros/tcp)"""
    os.makedirs(CSV_DIR, exist_ok=True)
    with open(CSV_FILENAME, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'fecha_hora',
            'tam_payload_bytes',
            'protocolo',
            'mensaje',  # ✨ NUEVA COLUMNA: contenido del mensaje enviado
            'rtt_promedio_ms',
            'rtt_desv_std_ms',
            'jitter_ms',
            'rx_mbps',
            'tx_mbps',
            'gateway'
        ])


def guardar_metricas_csv(payload_size, mensaje, protocolo="TCP"):
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
                mensaje,  # ✨ Guardar el mensaje enviado
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

    # -------------------------------------------------------------------------
    # NOTA DE SIMILITUD: Este servidor TCP está escrito para parecerse lo máximo
    # posible a `udp_server.py`. Las diferencias clave están marcadas con
    # "🔄 CAMBIO TCP↔UDP:". En resumen:
    #   - TCP: SOCK_STREAM, bind/listen/accept, conn.sendall()/conn.recv()
    #   - UDP: SOCK_DGRAM, bind, server.sendto()/server.recvfrom(), no accept
    # Mantuvimos idéntica la lógica de métricas, CSV y formato de mensajes.
    # -------------------------------------------------------------------------

    # 🔄 CAMBIO TCP↔UDP: creación del socket (TCP usa SOCK_STREAM)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(1)
    print(f"[INFO] Servidor TCP escuchando en {HOST}:{PORT}")

    # 🔄 CAMBIO TCP↔UDP: en TCP hay accept() que devuelve conn y addr
    conn, addr = server.accept()
    print(f"[INFO] Cliente conectado: {addr}")

    last_send = time.time()
    next_interval = random.uniform(INTERVAL_MIN, INTERVAL_MAX)
    conn.settimeout(0.1)

    try:
        while True:
            now = time.time()
            # Enviar carga aleatoria cuando toque
            if now - last_send >= next_interval:
                payload = random_payload()
                try:
                    conn.sendall((payload + "\n").encode())

                    # MEDIR Y GUARDAR MÉTRICAS (lo que pide el PDF) + el mensaje
                    metricas = guardar_metricas_csv(len(payload), payload)

                    print(f"[SEND] '{payload}' ({len(payload)} bytes)  "
                          f"RTT: {metricas.get('rtt_avg_ms', 'N/A')}ms  "
                          f"Jitter: {metricas.get('jitter_ms', 'N/A')}ms  "
                          f"Next: {next_interval:.2f}s")

                except (BrokenPipeError, ConnectionResetError):
                    print("[INFO] Cliente desconectado durante send.")
                    break

                last_send = now
                next_interval = random.uniform(INTERVAL_MIN, INTERVAL_MAX)

            # Recepción no bloqueante para eco
            try:
                data = conn.recv(1024)
                if not data:
                    print("[INFO] Cliente cerró la conexión.")
                    break
                conn.sendall(data)  # Eco
            except socket.timeout:
                pass

    except KeyboardInterrupt:
        print("\n[INFO] Servidor interrumpido por usuario")
    finally:
        conn.close()
        server.close()
        print("[INFO] Servidor detenido.")
        print(f"[INFO] Datos guardados en: {CSV_FILENAME}")


if __name__ == "__main__":
    main()
