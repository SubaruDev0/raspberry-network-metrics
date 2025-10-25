#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

# Configuración de carpetas
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTROS_DIR = os.path.join(PROJECT_ROOT, 'registros')
GRAFICOS_DIR = os.path.join(PROJECT_ROOT, 'graficos', 'server')

# Crear carpeta si no existe
os.makedirs(GRAFICOS_DIR, exist_ok=True)

# Configuración de matplotlib
plt.rcParams['font.size'] = 10
plt.rcParams['figure.figsize'] = (12, 8)


def cargar_datos_servidor():
    """Carga datos del servidor"""
    try:
        servidor_csv = os.path.join(REGISTROS_DIR, 'metricas_servidor.csv')
        df_servidor = pd.read_csv(servidor_csv)

        print(f"[INFO] Datos del servidor cargados: {len(df_servidor)} registros")

        # Convertir timestamp y calcular tiempo
        df_servidor['datetime'] = pd.to_datetime(df_servidor['fecha_hora'])
        inicio = df_servidor['datetime'].min()
        df_servidor['tiempo_segundos'] = (df_servidor['datetime'] - inicio).dt.total_seconds()

        # Filtrar registros válidos
        df_servidor = df_servidor[df_servidor['tam_payload_bytes'] > 0]

        return df_servidor

    except Exception as e:
        print(f"[ERROR] No se pudieron cargar los datos del servidor: {e}")
        return None


def generar_graficos_servidor(df_servidor):
    """Genera gráficos específicos del servidor"""
    print("\n--- GENERANDO GRÁFICOS DEL SERVIDOR ---")

    # 1. RTT vs Tiempo
    plt.figure(figsize=(12, 6))
    plt.plot(df_servidor['tiempo_segundos'], df_servidor['rtt_promedio_ms'],
             'b-o', markersize=4, linewidth=2, alpha=0.8, label='RTT')

    rtt_avg = df_servidor['rtt_promedio_ms'].mean()
    plt.axhline(y=rtt_avg, color='r', linestyle='--',
                label=f'Promedio: {rtt_avg:.2f} ms')

    plt.title('RTT vs Tiempo - Servidor TCP', fontsize=14, fontweight='bold')
    plt.ylabel('RTT (ms)', fontsize=12)
    plt.xlabel('Tiempo (segundos)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(GRAFICOS_DIR, 'rtt_vs_tiempo.png'), dpi=300)
    plt.close()
    print("✅ rtt_vs_tiempo.png")

    # 2. Payload vs RTT
    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(df_servidor['tam_payload_bytes'],
                          df_servidor['rtt_promedio_ms'],
                          c=df_servidor['jitter_ms'],
                          cmap='viridis', alpha=0.7, s=60)

    plt.colorbar(scatter, label='Jitter (ms)')
    plt.title('Tamaño de Payload vs RTT - Servidor TCP', fontsize=14, fontweight='bold')
    plt.xlabel('Tamaño de Payload (bytes)', fontsize=12)
    plt.ylabel('RTT Promedio (ms)', fontsize=12)
    plt.grid(True, alpha=0.3)

    correlacion = df_servidor['tam_payload_bytes'].corr(df_servidor['rtt_promedio_ms'])
    plt.text(0.05, 0.95, f'Correlación: {correlacion:.3f}',
             transform=plt.gca().transAxes, fontsize=12,
             bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))

    plt.tight_layout()
    plt.savefig(os.path.join(GRAFICOS_DIR, 'payload_vs_rtt.png'), dpi=300)
    plt.close()
    print("✅ payload_vs_rtt.png")

    # 3. Jitter vs Tiempo
    plt.figure(figsize=(12, 6))
    plt.plot(df_servidor['tiempo_segundos'], df_servidor['jitter_ms'],
             'r-o', markersize=4, linewidth=2, alpha=0.8, label='Jitter')

    jitter_avg = df_servidor['jitter_ms'].mean()
    plt.axhline(y=jitter_avg, color='orange', linestyle='--',
                label=f'Promedio: {jitter_avg:.2f} ms')

    plt.title('Jitter vs Tiempo - Servidor TCP', fontsize=14, fontweight='bold')
    plt.ylabel('Jitter (ms)', fontsize=12)
    plt.xlabel('Tiempo (segundos)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(GRAFICOS_DIR, 'jitter_vs_tiempo.png'), dpi=300)
    plt.close()
    print("✅ jitter_vs_tiempo.png")


def main():
    """Función principal"""
    print("Generador de Gráficos - Servidor")
    print("=" * 40)

    df_servidor = cargar_datos_servidor()
    if df_servidor is None:
        print("[ERROR] No hay datos del servidor para generar gráficos")
        return

    generar_graficos_servidor(df_servidor)
    print(f"\n✅ Gráficos del servidor guardados en: {GRAFICOS_DIR}")


if __name__ == "__main__":
    main()