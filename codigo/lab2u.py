
''' Descomentar en la U xd
"""
Métricas disponibles (nombres para usar en METRICS):
  "ssid", "ip", "gateway",
  "rssi_dbm", "tx_bitrate_mbps", "rx_bitrate_mbps",
  "freq_mhz", "channel", "link_quality",
  "rtt_avg_ms", "rtt_std_ms", "jitter_ms",
  "rx_mbps", "tx_mbps"
"""

import subprocess, time, shutil, json, re
from typing import Optional, Tuple, Dict, Any

# ===========================
# HARD-CODE CONFIG (editame)
# ===========================
IFACE = "wlan0"                    # Interfaz de red WiFi
WIFI_SSID = "Sala_Hibrida"     # SSID de la red a conectar
WIFI_PSK  = "USSqiDyJ25"      # Contraseña de la red

# Elige qué métricas medir (solo estas se calcularán)
METRICS = [
    # Identidad/red
    "ssid", "ip", "gateway",
    # Radio/enlace
    "rssi_dbm", "tx_bitrate_mbps", "rx_bitrate_mbps", "freq_mhz", "channel", "link_quality",
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


# ------------------------------- Conexión ------------------------------- #

def connect_wifi(ssid: str, psk: Optional[str], iface: str, timeout_s: int = 30) -> bool:
    """Conecta a una red Wi-Fi usando nmcli (si existe)."""
    if not _cmd_exists("nmcli"):
        print("[WARN] nmcli no disponible; saltando conexión.")
        return False

    if psk:
        code, out, err = _run(f'nmcli dev wifi connect "{ssid}" password "{psk}" ifname {iface}')
    else:
        code, out, err = _run(f'nmcli dev wifi connect "{ssid}" ifname {iface}')
    if code != 0:
        print(f"[ERR] nmcli connect: {err or out}")

    t0 = time.time()
    while time.time() - t0 < timeout_s:
        ssid_now = _get_wifi_ssid(iface)
        if ssid_now == ssid:
            return True
        time.sleep(1)
    return False


# ------------------------------ Lectores base --------------------------- #

def _get_wifi_ssid(iface: str) -> Optional[str]:
    """Obtiene el SSID de la red WiFi conectada usando el comando iw"""
    if not _cmd_exists("iw"):
        return None
    code, out, _ = _run(f"iw dev {iface} link")
    if code != 0 or not out:
        return None
    m = re.search(r"SSID:\s*(.+)", out)
    return m.group(1).strip() if m else None

def _get_wifi_status(iface: str) -> Dict[str, Any]:
    """Retorna dict con: ssid, freq_mhz, tx_bitrate_mbps, rx_bitrate_mbps, rssi_dbm, link_quality, channel."""
    res: Dict[str, Any] = {
        "ssid": None, "freq_mhz": None, "tx_bitrate_mbps": None, "rx_bitrate_mbps": None,
        "rssi_dbm": None, "link_quality": None, "channel": None
    }
    if not _cmd_exists("iw"):
        return res

    code, out, _ = _run(f"iw dev {iface} link")
    if code != 0 or not out:
        return res

    # Extrae información usando expresiones regulares
    ssid = re.search(r"SSID:\s*(.+)", out)
    freq = re.search(r"freq:\s*(\d+)", out)
    txb  = re.search(r"tx bitrate:\s*([\d\.]+)\s*MBit/s", out)
    rxb  = re.search(r"rx bitrate:\s*([\d\.]+)\s*MBit/s", out)
    sig  = re.search(r"signal:\s*([-]?\d+)\s*dBm", out)

    res["ssid"] = ssid.group(1).strip() if ssid else None
    res["freq_mhz"] = int(freq.group(1)) if freq else None
    res["tx_bitrate_mbps"] = float(txb.group(1)) if txb else None
    res["rx_bitrate_mbps"] = float(rxb.group(1)) if rxb else None
    res["rssi_dbm"] = float(sig.group(1)) if sig else None
    res["channel"] = _parse_channel(res["freq_mhz"])

    # /proc/net/wireless -> calidad 0..1
    try:
        with open("/proc/net/wireless") as f:
            for line in f:
                if iface in line:
                    parts = line.split()
                    qual = parts[2].replace(".", "")
                    q = float(qual) if qual else 0.0
                    res["link_quality"] = max(0.0, min(q / 70.0, 1.0))
                    break
    except Exception:
        pass

    return res

def _parse_channel(freq_mhz: Optional[int]) -> Optional[int]:
    """Convierte frecuencia MHz a canal WiFi"""
    if not freq_mhz:
        return None
    if 2400 <= freq_mhz <= 2500:
        return int(round((freq_mhz - 2412) / 5.0 + 1))
    if 5000 <= freq_mhz <= 6000:
        return int(round((freq_mhz - 5000) / 5.0))
    if 5900 <= freq_mhz <= 7125:
        return int(round((freq_mhz - 5950) / 5.0))  # aprox 6 GHz
    return None

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

    # Conexión (si no estás conectado, intenta conectarte)
    if "ssid" in METRICS or any(k in METRICS for k in
                                ["rssi_dbm","tx_bitrate_mbps","rx_bitrate_mbps","freq_mhz","channel","link_quality"]):
        # Intento de conexión rápida (no falla si ya está conectado)
        connect_wifi(WIFI_SSID, WIFI_PSK, IFACE)

    # WIFI status (si se pide cualquiera de las métricas de radio o ssid)
    if any(k in METRICS for k in ["ssid","rssi_dbm","tx_bitrate_mbps","rx_bitrate_mbps","freq_mhz","channel","link_quality"]):
        wifi = _get_wifi_status(IFACE)
        for k in ["ssid","rssi_dbm","tx_bitrate_mbps","rx_bitrate_mbps","freq_mhz","channel","link_quality"]:
            if k in METRICS:
                results[k] = wifi.get(k)

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
'''