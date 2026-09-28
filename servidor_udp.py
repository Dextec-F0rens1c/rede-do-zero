import socket
import sys

HOST = "0.0.0.0"
PORT = 6000


def servidor():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))
    print(f"Servidor UDP ouvindo em {HOST}:{PORT}")

    while True:
        dados, addr = sock.recvfrom(1024)
        texto = dados.decode("utf-8", errors="ignore")
        print(f"[{addr[0]}:{addr[1]}] {texto}")
        sock.sendto(f"eco: {texto}".encode("utf-8"), addr)


def cliente(mensagem):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(3)
    sock.sendto(mensagem.encode("utf-8"), ("127.0.0.1", PORT))
    try:
        dados, _ = sock.recvfrom(1024)
        print(f"Resposta: {dados.decode('utf-8', errors='ignore')}")
    except socket.timeout:
        print("Timeout. UDP nao garante entrega, igual a diferenca para o TCP.")
    sock.close()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "servidor":
        servidor()
    else:
        cliente(sys.argv[1] if len(sys.argv) > 1 else "ola UDP")
