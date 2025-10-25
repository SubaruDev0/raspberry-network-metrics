#!/usr/bin/env python3
import socket
import time
import random
import string
import csv
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

# Archivo CSV para guardar resultados
CSV_FILENAME = "metricas_servidor.csv"


def random_payload():
    """Genera mensaje aleatorio como pide el PDF"""
    size = random.randint(MIN_LEN, MAX_LEN)
    return ''.join(random.choices(string.ascii_letters + string.digits, k=size))


def inicializar_csv():
    """Crea el archivo CSV con los headers"""
    with open(CSV_FILENAME, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'timestamp', 'payload_size', 'protocolo',
            'rtt_avg_ms', 'rtt_std_ms', 'jitter_ms',
            'rx_mbps', 'tx_mbps', 'gateway'
        ])


def guardar_metricas_csv(payload_size, protocolo="TCP"):
    """Guarda métricas actuales en el CSV"""
    try:
        # Obtener métricas de red
        metricas = get_network_metrics_filtered()

        with open(CSV_FILENAME, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().isoformat(),
                payload_size,
                protocolo,
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

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(1)
    print(f"[INFO] Servidor escuchando en {HOST}:{PORT}")

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

                    # MEDIR Y GUARDAR MÉTRICAS (lo que pide el PDF)
                    metricas = guardar_metricas_csv(len(payload))

                    print(f"[SEND] {len(payload)} bytes | "
                          f"RTT: {metricas.get('rtt_avg_ms', 'N/A')}ms | "
                          f"Jitter: {metricas.get('jitter_ms', 'N/A')}ms | "
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