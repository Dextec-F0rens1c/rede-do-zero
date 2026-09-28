import socket
import struct
import sys

HOST = "127.0.0.1"
PORT = 6767
XID = 0xAABBCCDD
MAC = sys.argv[1] if len(sys.argv) > 1 else "aa:bb:cc:dd:ee:01"


def enviar(sock, tipo, ip, mensagem):
    mac_bytes = bytes(int(p, 16) for p in MAC.split(":"))
    ip_bytes = socket.inet_aton(ip)
    cab = struct.pack("!BBBBIHH", 1, 1, 6, tipo, XID, 0, 0x8000)
    pacote = cab + mac_bytes + b"\x00" * 4 + ip_bytes + b"\x00" * 4 + mensagem.encode() + b"\x00" * 16
    sock.sendto(pacote, (HOST, PORT))


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(3)
    print(f"Dispositivo {MAC} iniciando requisicao de endereco IP\n")

    enviar(sock, 1, "0.0.0.0", "DISCOVERY")
    print("1) DISCOVER enviado -> perguntando a rede: alguem tem IP pra mim?")

    try:
        dados, _ = sock.recvfrom(2048)
        print(f"2) Recebi resposta: {dados[26:].rstrip(b'\\x00').decode('utf-8', errors='ignore')}")
    except socket.timeout:
        print("Sem resposta do servidor DHCP")
        return

    enviar(sock, 3, "0.0.0.0", "REQUEST")
    print("3) REQUEST enviado -> aceito a oferta")

    try:
        dados, _ = sock.recvfrom(2048)
        ip_final = socket.inet_ntoa(dados[22:26])
        print(f"4) Recebi ACK -> meu IP e {ip_final}")
    except socket.timeout:
        print("Sem ACK do servidor DHCP")

    sock.close()


if __name__ == "__main__":
    main()
