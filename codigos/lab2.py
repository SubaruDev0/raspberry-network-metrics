#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Métricas disponibles (nombres para usar en METRICS):
  "ip", "gateway",
  "rtt_avg_ms", "rtt_std_ms", "jitter_ms",
  "rx_mbps", "tx_mbps"
"""

import subprocess, time, shutil, json, re
from typing import Optional, Tuple, Dict, Any

# ===========================
# CONFIGURACIÓN PARA CASA (Cable Ethernet)
# ===========================
IFACE = "eth0"                    # Interfaz de red por cable

# Elige qué métricas medir (solo estas se calcularán)
METRICS = [
    # Identidad/red
    "ip", "gateway",
    # Latencia/variabilidad
    "rtt_avg_ms", "rtt_std_ms", "jitter_ms",
    # Throughput interfaz (ventana)
    "rx_mbps", "tx_mbps",
]

# Destino para RTT/Jitter (None => gateway por defecto)
RTT_TARGET = None
# Conteo de pings para medir RTT
RTT_COUNT = 10
# Ventana (s) para estimar throughput leyendo /proc/net/dev
THR_WINDOW_S = 1.0


# ----------------------------- Utilidades OS ----------------------------- #

def _cmd_exists(name: str) -> bool:
    """Verifica si un comando del sistema existe"""
    return shutil.which(name) is not None

def _run(cmd: str, timeout: int = 10):
    """Ejecuta un comando del sistema con timeout"""
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        out, err = p.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        p.kill()
        return 124, "", "timeout"
    return p.returncode, out.strip(), err.strip()


# ------------------------------ Lectores base --------------------------- #

def _get_ip_and_gateway(iface: str) -> Tuple[Optional[str], Optional[str]]:
    """Obtiene IP y gateway de la interfaz"""
    ip_addr, gw = None, None
    code, out, _ = _run(f"ip -4 addr show dev {iface}")
    if code == 0:
        m = re.search(r"inet\s+(\d+\.\d+\.\d+\.\d+)", out)
        if m: ip_addr = m.group(1)
    code, out, _ = _run("ip route show default")
    if code == 0:
        m = re.search(r"default via (\d+\.\d+\.\d+\.\d+)", out)
        if m: gw = m.group(1)
    return ip_addr, gw

def _estimate_rtt_and_jitter(target: str, count: int, interval_s: float = 0.2):
    """Retorna (rtt_avg_ms, rtt_std_ms, jitter_ms) usando ping."""
    if not _cmd_exists("ping"):
        return None, None, None
    code, out, _ = _run(f"ping -n -i {interval_s} -c {count} {target}", timeout=int(count*interval_s)+10)
    if code != 0 or not out:
        return None, None, None
    rtts = [float(x) for x in re.findall(r"time=([\d\.]+)\s*ms", out)]
    if not rtts:
        return None, None, None
    avg = sum(rtts) / len(rtts)
    mean = avg
    var = sum((x - mean) ** 2 for x in rtts) / len(rtts)
    std = var ** 0.5
    deltas = [abs(rtts[i] - rtts[i-1]) for i in range(1, len(rtts))]
    jitter = sum(deltas) / len(deltas) if deltas else 0.0
    return avg, std, jitter

def _read_proc_net_dev() -> dict:
    """Lee estadísticas de red desde /proc/net/dev"""
    stats = {}
    with open("/proc/net/dev") as f:
        for line in f:
            if ":" not in line:
                continue
            iface, rest = line.split(":")
            iface = iface.strip()
            cols = rest.split()
            try:
                stats[iface] = (int(cols[0]), int(cols[8]))  # rx_bytes, tx_bytes
            except Exception:
                pass
    return stats

def _estimate_iface_throughput(iface: str, window_s: float):
    """Estima throughput midiendo bytes transferidos en una ventana de tiempo"""
    s0 = _read_proc_net_dev()
    if iface not in s0: return None, None
    time.sleep(window_s)
    s1 = _read_proc_net_dev()
    if iface not in s1: return None, None
    rx_b = s1[iface][0] - s0[iface][0]
    tx_b = s1[iface][1] - s0[iface][1]
    rx_mbps = (rx_b * 8) / window_s / 1e6
    tx_mbps = (tx_b * 8) / window_s / 1e6
    return rx_mbps, tx_mbps


# ------------------------- Selector por METRICS ------------------------- #

def get_network_metrics_filtered() -> Dict[str, Any]:
    """
    Ejecuta solo las mediciones presentes en METRICS y retorna un dict con esas keys.
    """
    results: Dict[str, Any] = {}

    # IP y gateway
    if "ip" in METRICS or "gateway" in METRICS or any(k in METRICS for k in ["rtt_avg_ms","rtt_std_ms","jitter_ms"]):
        ip, gw = _get_ip_and_gateway(IFACE)
        if "ip" in METRICS: results["ip"] = ip
        if "gateway" in METRICS: results["gateway"] = gw

    # RTT/Jitter
    if any(k in METRICS for k in ["rtt_avg_ms","rtt_std_ms","jitter_ms"]):
        target = RTT_TARGET or results.get("gateway")
        if target:
            avg, std, jit = _estimate_rtt_and_jitter(target, count=RTT_COUNT)
        else:
            avg = std = jit = None
        if "rtt_avg_ms" in METRICS: results["rtt_avg_ms"] = avg
        if "rtt_std_ms" in METRICS: results["rtt_std_ms"] = std
        if "jitter_ms"  in METRICS: results["jitter_ms"]  = jit

    # Throughput por ventana
    if "rx_mbps" in METRICS or "tx_mbps" in METRICS:
        rx, tx = _estimate_iface_throughput(IFACE, THR_WINDOW_S)
        if "rx_mbps" in METRICS: results["rx_mbps"] = rx
        if "tx_mbps" in METRICS: results["tx_mbps"] = tx

    return results


# --------------------------------- CLI ---------------------------------- #

def main():
    """Función principal para uso desde línea de comandos"""
    import argparse
    ap = argparse.ArgumentParser(description="Código 1 (hardcode): métricas filtradas")
    ap.add_argument("--json", action="store_true", help="Imprime JSON con las métricas seleccionadas")
    args = ap.parse_args()

    res = get_network_metrics_filtered()
    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        for k, v in res.items():
            print(f"{k}: {v}")

if __name__ == "__main__":
    main()
