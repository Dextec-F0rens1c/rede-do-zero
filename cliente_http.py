import socket

HOST = "127.0.0.1"
PORT = 8080
ALVO = "/index.html"


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    requisicao = (
        f"GET {ALVO} HTTP/1.1\r\n"
        f"Host: {HOST}:{PORT}\r\n"
        "User-Agent: cliente-bruto/1.0\r\n"
        "Connection: close\r\n"
        "\r\n"
    )
    sock.sendall(requisicao.encode("utf-8"))

    bruto = b""
    while True:
        pedaco = sock.recv(4096)
        if not pedaco:
            break
        bruto += pedaco
    sock.close()

    cabecalho, _, corpo = bruto.partition(b"\r\n\r\n")
    print("=== CABECALHOS DA RESPOSTA ===")
    print(cabecalho.decode("utf-8", errors="ignore"))
    print("\n=== CORPO (HTML) ===")
    print(corpo.decode("utf-8", errors="ignore"))


if __name__ == "__main__":
    main()
