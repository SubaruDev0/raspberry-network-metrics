#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de Gráficos - Cliente UDP
Genera visualizaciones de las métricas capturadas por el cliente UDP
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Configuración de carpetas
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTROS_DIR = os.path.join(PROJECT_ROOT, 'registros', 'udp')
GRAFICOS_DIR = os.path.join(PROJECT_ROOT, 'graficos', 'udp', 'cliente')

# Crear carpeta si no existe
os.makedirs(GRAFICOS_DIR, exist_ok=True)

# Configuración de matplotlib
plt.rcParams['font.size'] = 10
plt.rcParams['figure.figsize'] = (12, 8)


def cargar_datos_cliente():
    """Carga datos del cliente UDP"""
    try:
        cliente_csv = os.path.join(REGISTROS_DIR, 'metricas_cliente.csv')
        df_cliente = pd.read_csv(cliente_csv)

        print(f"[INFO] Datos del cliente UDP cargados: {len(df_cliente)} registros")

        # Convertir timestamp y calcular tiempo
        df_cliente['datetime'] = pd.to_datetime(df_cliente['fecha_hora'])
        inicio = df_cliente['datetime'].min()
        df_cliente['tiempo_segundos'] = (df_cliente['datetime'] - inicio).dt.total_seconds()

        # Filtrar registros válidos
        df_cliente = df_cliente[df_cliente['tam_mensaje_bytes'] > 0]

        return df_cliente

    except Exception as e:
        print(f"[ERROR] No se pudieron cargar los datos del cliente UDP: {e}")
        return None


def generar_graficos_cliente(df_cliente):
    """Genera gráficos específicos del cliente UDP"""
    print("\n--- GENERANDO GRÁFICOS DEL CLIENTE UDP ---")

    # 1. RTT vs Tiempo
    plt.figure(figsize=(12, 6))
    plt.plot(df_cliente['tiempo_segundos'], df_cliente['rtt_promedio_ms'],
             'g-o', markersize=4, linewidth=2, alpha=0.8, label='RTT')

    rtt_avg = df_cliente['rtt_promedio_ms'].mean()
    plt.axhline(y=rtt_avg, color='r', linestyle='--',
                label=f'Promedio: {rtt_avg:.2f} ms')

    plt.title('RTT vs Tiempo - Cliente UDP', fontsize=14, fontweight='bold')
    plt.ylabel('RTT (ms)', fontsize=12)
    plt.xlabel('Tiempo (segundos)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(GRAFICOS_DIR, 'rtt_vs_tiempo.png'), dpi=300)
    plt.close()
    print("✅ rtt_vs_tiempo.png")

    # 2. Jitter vs Tiempo
    plt.figure(figsize=(12, 6))
    plt.plot(df_cliente['tiempo_segundos'], df_cliente['jitter_ms'],
             'm-o', markersize=4, linewidth=2, alpha=0.8, label='Jitter')

    jitter_avg = df_cliente['jitter_ms'].mean()
    plt.axhline(y=jitter_avg, color='orange', linestyle='--',
                label=f'Promedio: {jitter_avg:.2f} ms')

    plt.title('Jitter vs Tiempo - Cliente UDP', fontsize=14, fontweight='bold')
    plt.ylabel('Jitter (ms)', fontsize=12)
    plt.xlabel('Tiempo (segundos)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(GRAFICOS_DIR, 'jitter_vs_tiempo.png'), dpi=300)
    plt.close()
    print("✅ jitter_vs_tiempo.png")

    # 3. Throughput vs Tiempo
    plt.figure(figsize=(12, 6))
    plt.plot(df_cliente['tiempo_segundos'], df_cliente['throughput_recepcion_mbps'],
             'c-o', markersize=4, linewidth=2, alpha=0.8, label='Throughput')

    throughput_avg = df_cliente['throughput_recepcion_mbps'].mean()
    plt.axhline(y=throughput_avg, color='purple', linestyle='--',
                label=f'Promedio: {throughput_avg:.4f} Mbps')

    plt.title('Throughput de Recepción vs Tiempo - Cliente UDP', fontsize=14, fontweight='bold')
    plt.ylabel('Throughput (Mbps)', fontsize=12)
    plt.xlabel('Tiempo (segundos)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(GRAFICOS_DIR, 'throughput_vs_tiempo.png'), dpi=300)
    plt.close()
    print("✅ throughput_vs_tiempo.png")


def main():
    """Función principal"""
    print("Generador de Gráficos - Cliente UDP")
    print("=" * 40)

    df_cliente = cargar_datos_cliente()
    if df_cliente is None:
        print("[ERROR] No hay datos del cliente UDP para generar gráficos")
        return

    generar_graficos_cliente(df_cliente)
    print(f"\n✅ Gráficos del cliente UDP guardados en: {GRAFICOS_DIR}")


if __name__ == "__main__":
    main()

