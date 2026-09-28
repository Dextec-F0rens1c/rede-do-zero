import socket
import threading

HOST = "0.0.0.0"
PORT = 5000

clientes = []
lock = threading.Lock()


def transmitir(texto):
    with lock:
        for c in list(clientes):
            try:
                c.sendall(texto.encode("utf-8"))
            except OSError:
                clientes.remove(c)
                c.close()


def tratar_cliente(conn, addr):
    print(f"[+] Entnou: {addr[0]}:{addr[1]}")
    with lock:
        clientes.append(conn)

    try:
        while True:
            msg = conn.recv(1024).decode("utf-8", errors="ignore")
            if not msg:
                break
            print(f"    {msg}")
            transmitir(f"{addr[0]} disse: {msg}\n")
    except OSError:
        pass
    finally:
        with lock:
            if conn in clientes:
                clientes.remove(conn)
        conn.close()
        print(f"[-] Saiu: {addr[0]}:{addr[1]}")


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Servidor TCP ouvindo em {HOST}:{PORT}")
    print("Aguardando clientes...\n")

    while True:
        conn, addr = server.accept()
        print(f"[+] Conexao estabelecida (SYN/ACK aceito)")
        threading.Thread(target=tratar_cliente, args=(conn, addr), daemon=True).start()


if __name__ == "__main__":
    main()
