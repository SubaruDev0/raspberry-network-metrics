#!/usr/bin/env python3
import socket
import sys
import select

HOST = "127.0.0.1" #"10.200.210.128"
PORT = 5000

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    sock.setblocking(False)  # No bloquea en recv
    print(f"[INFO] Conectado a {HOST}:{PORT}")
    print("Escribe mensajes y presiona Enter (o 'exit' para salir)")

    while True:
        read_sockets, _, _ = select.select([sock, sys.stdin], [], [])

        for s in read_sockets:
            if s == sock:
                try:
                    data = sock.recv(1024)
                    if data:
                        print(f"[SRV] {data.decode().strip()}")
                    else:
                        print("[INFO] Servidor cerró la conexión")
                        return
                except BlockingIOError:
                    pass

            elif s == sys.stdin:
                msg = sys.stdin.readline().strip()
                if msg.lower() == "exit":
                    sock.close()
                    return
                sock.sendall((msg + "\n").encode())

if __name__ == "__main__":
    main()
