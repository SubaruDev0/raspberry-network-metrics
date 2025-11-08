# 🌐 Raspberry Network Metrics - Laboratorio 2 Redes

Sistema completo de monitoreo y análisis de métricas de red para comunicación Cliente-Servidor usando **TCP** y **UDP**.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-success)

---

## 📋 Tabla de Contenidos

- [Descripción](#-descripción)
- [Características](#-características)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Requisitos](#-requisitos)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Diferencias TCP vs UDP](#-diferencias-tcp-vs-udp)
- [Métricas Capturadas](#-métricas-capturadas)
- [Gráficos Generados](#-gráficos-generados)
- [Configuración](#-configuración)
- [Troubleshooting](#-troubleshooting)

---

## 🎯 Descripción

Este proyecto implementa un sistema distribuido de medición de métricas de red entre dos Raspberry Pi (o cualquier sistema Linux). Permite analizar el rendimiento de la red en tiempo real capturando métricas como RTT, jitter, throughput y más.

### ¿Qué hace este proyecto?

1. **Servidor**: Envía mensajes aleatorios a intervalos variables al cliente
2. **Cliente**: Recibe mensajes y responde (eco)
3. **Métricas**: Ambos capturan métricas de red en cada transacción
4. **Visualización**: Genera gráficos automáticamente para análisis
5. **Protocolos**: Soporta tanto **TCP** (confiable) como **UDP** (rápido)

---

## ✨ Características

- ✅ **Doble Protocolo**: TCP y UDP completamente implementados
- ✅ **Separación Clara**: Archivos y carpetas organizados por protocolo
- ✅ **Métricas Completas**: RTT, Jitter, Throughput, y más
- ✅ **Registro de Mensajes**: Columna extra en CSV con el contenido enviado/recibido
- ✅ **Visualización Automática**: Gráficos PNG de alta calidad
- ✅ **Menú Interactivo**: Interfaz de usuario colorida y fácil de usar
- ✅ **Datos en CSV**: Exportación lista para análisis en Excel/Python

---

## 📁 Estructura del Proyecto

```
raspberry-network-metrics/
│
├── codigos/                          # Código fuente
│   ├── main.py                       # 🎮 Menú principal interactivo
│   ├── lab2.py                       # 🔧 Librería de métricas de red
│   │
│   ├── tcp_cliente.py                # 🔵 Cliente TCP
│   ├── tcp_server.py                 # 🔵 Servidor TCP
│   ├── udp_cliente.py                # 🟢 Cliente UDP
│   ├── udp_server.py                 # 🟢 Servidor UDP
│   │
│   ├── graficos_tcp_cliente.py       # 📊 Gráficos TCP Cliente
│   ├── graficos_tcp_servidor.py      # 📊 Gráficos TCP Servidor
│   ├── graficos_udp_cliente.py       # 📊 Gráficos UDP Cliente
│   └── graficos_udp_servidor.py      # 📊 Gráficos UDP Servidor
│
├── registros/                        # Datos capturados (CSV)
│   ├── tcp/
│   │   ├── metricas_cliente.csv      # Datos del cliente TCP
│   │   └── metricas_servidor.csv     # Datos del servidor TCP
│   └── udp/
│       ├── metricas_cliente.csv      # Datos del cliente UDP
│       └── metricas_servidor.csv     # Datos del servidor UDP
│
├── graficos/                         # Gráficos generados (PNG)
│   ├── tcp/
│   │   ├── cliente/                  # Gráficos del cliente TCP
│   │   └── server/                   # Gráficos del servidor TCP
│   └── udp/
│       ├── cliente/                  # Gráficos del cliente UDP
│       └── server/                   # Gráficos del servidor UDP
│
├── documentacion/
│   └── Evaluacion Lab 2 Redes.pdf    # Especificación del proyecto
│
├── requirements.txt                  # Dependencias Python
└── README.md                         # Este archivo
```

---

## 🔧 Requisitos

### Hardware
- 2 Raspberry Pi (o cualquier sistema Linux)
- Conexión de red entre ambos (Ethernet o WiFi)

### Software
- **Python 3.8+**
- **Linux** (probado en Raspberry Pi OS)
- Permisos para ejecutar comandos de red (`ping`, `ip`)

### Librerías Python
```bash
pandas>=1.5.0
matplotlib>=3.5.0
```

---

## 📦 Instalación

### 1. Clonar o descargar el proyecto

```bash
cd ~/Escritorio/Proyectos
git clone <tu-repositorio> raspberry-network-metrics
cd raspberry-network-metrics
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

O manualmente:

```bash
pip install pandas matplotlib
```

### 3. Verificar permisos

Asegúrate de que los scripts tengan permisos de ejecución:

```bash
chmod +x codigos/*.py
```

---

## 🚀 Uso

### Inicio Rápido

1. **En la Raspberry Pi del SERVIDOR** (Raspberry A):
   ```bash
   cd codigos/
   python3 main.py
   # Selecciona: 1 (Modo Servidor) → 1 (TCP) o 2 (UDP) → 1 (Ejecutar)
   ```

2. **En la Raspberry Pi del CLIENTE** (Raspberry B):
   ```bash
   cd codigos/
   python3 main.py
   # Selecciona: 2 (Modo Cliente) → 1 (TCP) o 2 (UDP) → 1 (Ejecutar)
   ```

### Menú Principal

El sistema tiene un menú interactivo con colores:

```
═══════════════════════════════════════════════════════════════════
     LABORATORIO 2 - REDES DE COMPUTADORES
═══════════════════════════════════════════════════════════════════
Selecciona el modo de ejecución:
1. 🖥️  MODO SERVIDOR (Raspberry Pi A)
2. 💻 MODO CLIENTE (Raspberry Pi B)
0. ❌ Salir
───────────────────────────────────────────────────────────────────
📌 Ambos modos soportan TCP y UDP
```

### Flujo de Trabajo Completo

#### Para TCP:
1. **Servidor**: `main.py` → Servidor → TCP → Ejecutar Servidor TCP
2. **Cliente**: `main.py` → Cliente → TCP → Ejecutar Cliente TCP
3. Dejar correr por algunos minutos (se generan datos automáticamente)
4. Presionar `Ctrl+C` para detener
5. Generar gráficos desde el menú (opción 2)

#### Para UDP:
1. **Servidor**: `main.py` → Servidor → UDP → Ejecutar Servidor UDP
2. **Cliente**: `main.py` → Cliente → UDP → Ejecutar Cliente UDP
3. Igual proceso que TCP

---

## 🔄 Diferencias TCP vs UDP

Este proyecto implementa **ambos protocolos** con el mismo comportamiento, pero con las diferencias fundamentales de cada uno:

### 🔵 TCP (Transmission Control Protocol)

**Características:**
- ✅ **Orientado a conexión**: Establece una conexión antes de transmitir
- ✅ **Confiable**: Garantiza la entrega de todos los paquetes
- ✅ **Ordenado**: Los mensajes llegan en el orden enviado
- ✅ **Control de flujo**: Ajusta velocidad según la red

**En el código:**
```python
# TCP - Requiere conexión
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # SOCK_STREAM
sock.connect((HOST, PORT))                                # connect()
sock.sendall(data)                                        # sendall()
data = sock.recv(1024)                                    # recv()
```

**Usa TCP cuando:**
- Necesitas garantizar que todos los datos lleguen
- El orden de los mensajes es importante
- No te importa un poco más de latencia
- Ejemplo: Transferencia de archivos, mensajes de texto

### 🟢 UDP (User Datagram Protocol)

**Características:**
- ⚡ **Sin conexión**: Envía directamente sin establecer conexión
- ⚡ **Más rápido**: Menos overhead de protocolo
- ⚠️ **No confiable**: Los paquetes pueden perderse
- ⚠️ **Sin orden garantizado**: Pueden llegar desordenados

**En el código:**
```python
# UDP - Sin conexión
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # SOCK_DGRAM
# No hay connect()
sock.sendto(data, (HOST, PORT))                          # sendto()
data, addr = sock.recvfrom(1024)                         # recvfrom()
```

**Usa UDP cuando:**
- La velocidad es más importante que la confiabilidad
- Pérdida ocasional de datos es aceptable
- Necesitas broadcast o multicast
- Ejemplo: Streaming de video/audio, juegos online, DNS

### 📊 Comparación Visual

| Característica | TCP | UDP |
|----------------|-----|-----|
| Conexión | Sí (3-way handshake) | No |
| Confiabilidad | ✅ Garantizada | ❌ Best-effort |
| Orden | ✅ Garantizado | ❌ No garantizado |
| Velocidad | Más lento | ⚡ Más rápido |
| Overhead | Mayor | Menor |
| Puerto por defecto | 5000 | 5001 |
| Uso de memoria | Mayor | Menor |

### 💡 Cambios en el Código

Los **únicos cambios** entre las versiones TCP y UDP son:

1. **Tipo de socket**: `SOCK_STREAM` → `SOCK_DGRAM`
2. **Funciones de envío/recepción**:
   - TCP: `sendall()` / `recv()`
   - UDP: `sendto()` / `recvfrom()`
3. **Manejo de conexión**:
   - TCP: `connect()` / `accept()`
   - UDP: Directo con direcciones
4. **Puerto**: TCP usa 5000, UDP usa 5001

Todo lo demás (métricas, lógica, mensajes) es **idéntico**.

---

## 📊 Métricas Capturadas

### CSV del Servidor

Columnas en `registros/{tcp|udp}/metricas_servidor.csv`:

| Columna | Descripción | Ejemplo |
|---------|-------------|---------|
| `fecha_hora` | Timestamp ISO 8601 | 2025-11-07T22:47:53 |
| `tam_payload_bytes` | Tamaño del mensaje enviado | 14 |
| `protocolo` | TCP o UDP | TCP |
| **`mensaje`** | ✨ **Contenido del mensaje enviado** | aB3xK9pL2 |
| `rtt_promedio_ms` | RTT promedio | 2.127 |
| `rtt_desv_std_ms` | Desviación estándar del RTT | 0.119 |
| `jitter_ms` | Variación del RTT | 0.147 |
| `rx_mbps` | Throughput de recepción | 0.0 |
| `tx_mbps` | Throughput de transmisión | 0.0 |
| `gateway` | IP del gateway | 192.168.100.1 |

### CSV del Cliente

Columnas en `registros/{tcp|udp}/metricas_cliente.csv`:

| Columna | Descripción | Ejemplo |
|---------|-------------|---------|
| `fecha_hora` | Timestamp ISO 8601 | 2025-11-07T22:47:53 |
| `tam_mensaje_bytes` | Tamaño del mensaje recibido | 14 |
| `protocolo` | TCP o UDP | TCP |
| **`mensaje`** | ✨ **Contenido del mensaje recibido** | aB3xK9pL2 |
| `rtt_promedio_ms` | RTT promedio | 2.127 |
| `rtt_desv_std_ms` | Desviación estándar del RTT | 0.119 |
| `jitter_ms` | Variación del RTT | 0.147 |
| `rx_mbps` | Throughput de recepción | 0.0 |
| `tx_mbps` | Throughput de transmisión | 0.0 |
| `gateway` | IP del gateway | 192.168.100.1 |
| `throughput_recepcion_mbps` | Throughput acumulado | 0.0001 |
| `total_mensajes_recibidos` | Contador de mensajes | 1 |
| `total_bytes_recibidos` | Contador de bytes | 14 |

### ✨ Nueva Columna: `mensaje`

La columna `mensaje` fue agregada para registrar el contenido exacto de cada mensaje enviado/recibido. Esto permite:
- **Debugging**: Ver qué mensajes se enviaron
- **Análisis**: Correlacionar tamaño con rendimiento
- **Auditoría**: Trazabilidad completa de la comunicación

---

## 📈 Gráficos Generados

Los scripts de visualización generan automáticamente gráficos en formato PNG (300 DPI).

### Gráficos del Cliente

1. **`rtt_vs_tiempo.png`**
   - RTT (ms) vs Tiempo (s)
   - Línea de promedio
   - Color: Verde (TCP) / Verde (UDP)

2. **`jitter_vs_tiempo.png`**
   - Jitter (ms) vs Tiempo (s)
   - Línea de promedio
   - Color: Magenta

3. **`throughput_vs_tiempo.png`**
   - Throughput (Mbps) vs Tiempo (s)
   - Línea de promedio
   - Color: Cyan

### Gráficos del Servidor

1. **`rtt_vs_tiempo.png`**
   - RTT (ms) vs Tiempo (s)
   - Línea de promedio
   - Color: Azul

2. **`jitter_vs_tiempo.png`**
   - Jitter (ms) vs Tiempo (s)
   - Línea de promedio
   - Color: Rojo

3. **`payload_vs_rtt.png`**
   - Scatter plot: Tamaño vs RTT
   - Colormap por Jitter
   - Coeficiente de correlación

---

## ⚙️ Configuración

### Cambiar IPs

**Cliente TCP** (`tcp_cliente.py`):
```python
HOST = "127.0.0.1"  # Cambia a la IP del servidor
PORT = 5000
```

**Cliente UDP** (`udp_cliente.py`):
```python
HOST = "127.0.0.1"  # Cambia a la IP del servidor
PORT = 5001
```

### Cambiar Intervalos de Envío

En los servidores:
```python
INTERVAL_MIN = 1  # Mínimo 1 segundo
INTERVAL_MAX = 5  # Máximo 5 segundos
```

### Cambiar Tamaño de Mensajes

En los servidores:
```python
MIN_LEN = 5   # Mínimo 5 caracteres
MAX_LEN = 20  # Máximo 20 caracteres
```

### Configurar Interfaz de Red

En `lab2.py`:
```python
IFACE = "eth0"  # Cambia a "wlan0" para WiFi
```

---

## 🔍 Troubleshooting

### Problema: "Connection refused"

**Causa**: El servidor no está ejecutándose
**Solución**: Inicia primero el servidor, luego el cliente

### Problema: "Permission denied" en ping

**Causa**: Falta de permisos para ejecutar ping
**Solución**: 
```bash
sudo setcap cap_net_raw+ep $(which ping)
```

### Problema: "No module named 'pandas'"

**Causa**: Dependencias no instaladas
**Solución**:
```bash
pip install -r requirements.txt
```

### Problema: Los gráficos no se generan

**Causa**: No hay datos en los CSV
**Solución**: Ejecuta el servidor y cliente, deja correr algunos minutos

### Problema: "Address already in use"

**Causa**: El puerto ya está ocupado
**Solución**:
```bash
# Buscar y matar el proceso
sudo lsof -i :5000
sudo kill -9 <PID>
```

### Problema: Cliente UDP no recibe mensajes

**Causa**: El servidor UDP necesita conocer la dirección del cliente primero
**Solución**: Envía un mensaje desde el cliente antes (escribe cualquier cosa y presiona Enter)

---

## 🧪 Ejemplo de Sesión

### Terminal 1 (Servidor TCP):
```bash
$ python3 main.py
# Seleccionar: 1 → 1 → 1
[INFO] CSV inicializado: ../registros/tcp/metricas_servidor.csv
[INFO] Servidor TCP escuchando en 0.0.0.0:5000
[INFO] Cliente conectado: ('192.168.1.100', 54321)
[SEND] 'aB3xK9pL2' (9 bytes)  RTT: 2.127ms  Jitter: 0.147ms  Next: 3.45s
[SEND] 'xY7kLm' (6 bytes)  RTT: 2.233ms  Jitter: 1.058ms  Next: 2.11s
```

### Terminal 2 (Cliente TCP):
```bash
$ python3 main.py
# Seleccionar: 2 → 1 → 1
[INFO] CSV cliente inicializado: ../registros/tcp/metricas_cliente.csv
[INFO] Conectado a 192.168.1.50:5000
[SRV] aB3xK9pL2  Tamaño: 9 bytes  Mensajes: 1  Throughput: 0.0001 Mbps
[SRV] xY7kLm  Tamaño: 6 bytes  Mensajes: 2  Throughput: 0.0002 Mbps
```

---

## 📝 Notas Adicionales

### ¿Por qué separar TCP y UDP?

La separación en carpetas permite:
- ✅ **Comparación directa**: Puedes ejecutar ambos y comparar métricas
- ✅ **Sin confusión**: Sabes exactamente qué datos corresponden a qué protocolo
- ✅ **Organización**: Facilita el análisis y presentación de resultados

### Métricas de Red

El módulo `lab2.py` usa comandos del sistema:
- `ping`: Para RTT y Jitter
- `ip`: Para IP y Gateway
- `/proc/net/dev`: Para throughput

### Seguridad

Este proyecto es para **fines educativos**. En producción considera:
- Autenticación
- Cifrado (TLS/DTLS)
- Validación de datos
- Rate limiting

---

## 👥 Autores

Proyecto desarrollado para el **Laboratorio 2** del curso de **Redes de Computadores**.

---

## 📄 Licencia

Este proyecto es de código abierto para fines educativos.

---

## 🎓 Referencias

- [Socket Programming in Python](https://docs.python.org/3/library/socket.html)
- [TCP vs UDP](https://www.cloudflare.com/learning/ddos/glossary/tcp-ip/)
- [Network Metrics](https://en.wikipedia.org/wiki/Network_performance)

---

**¡Disfruta midiendo tu red! 📡🚀**

