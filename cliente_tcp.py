import socket
import threading

HOST = "127.0.0.1"
PORT = 5000


def receber(sock):
    while True:
        try:
            print("\n" + sock.recv(4096).decode("utf-8", errors="ignore"))
        except OSError:
            break


def main():
    nome = input("Seu nome: ").strip() or "anonimo"

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    print(f"Conectado como {nome}. Digite e aperte Enter. Ctrl+C para sair.\n")

    threading.Thread(target=receber, args=(sock,), daemon=True).start()

    while True:
        try:
            msg = input("> ")
            sock.sendall(f"[{nome}] {msg}\n".encode("utf-8"))
        except (KeyboardInterrupt, OSError):
            sock.close()
            print("\nConexao encerrada.")
            break


if __name__ == "__main__":
    main()
