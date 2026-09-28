import os
import socket

HOST = "0.0.0.0"
PORT = 8080
RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "www")

TIPOS = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "text/javascript; charset=utf-8",
    ".txt": "text/plain; charset=utf-8",
    ".png": "image/png",
}


def resposta(caminho):
    arquivo = "index.html" if caminho == "/" else caminho.lstrip("/")
    alvo = os.path.abspath(os.path.join(RAIZ, arquivo))

    if not alvo.startswith(os.path.abspath(RAIZ)) or not os.path.isfile(alvo):
        corpo = b"404 - Nao encontrado"
        cabecalho = f"HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\nContent-Length: {len(corpo)}\r\n\r\n"
        return cabecalho.encode() + corpo

    with open(alvo, "rb") as f:
        corpo = f.read()

    tipo = TIPOS.get(os.path.splitext(arquivo)[1], "application/octet-stream")
    cabecalho = f"HTTP/1.1 200 OK\r\nContent-Type: {tipo}\r\nContent-Length: {len(corpo)}\r\n\r\n"
    return cabecalho.encode() + corpo


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Servidor HTTP em http://{HOST}:{PORT}")
    print(f"Servindo arquivos de: {RAIZ}\n")

    while True:
        conn, addr = server.accept()
        bruto = conn.recv(4096).decode("utf-8", errors="ignore")
        linhas = bruto.splitlines()
        partes = linhas[0].split() if linhas else ["GET", "/"]

        print(f"[{addr[0]}] {partes[0]} {partes[1]}")

        caminho = partes[1] if len(partes) > 1 else "/"
        conn.sendall(resposta(caminho))
        conn.close()


if __name__ == "__main__":
    main()
