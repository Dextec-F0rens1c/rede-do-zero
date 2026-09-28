import ipaddress
import socket
import struct

HOST = "0.0.0.0"
PORT = 6767
XID = 0xAABBCCDD
POOL = [f"192.168.10.{i}" for i in range(10, 20)]

TIPO = {1: "DISCOVER", 2: "OFFER", 3: "REQUEST", 4: "ACK"}
ATRIBUIDOS = {}


def montar(tipo, mac, ip, mensagem):
    mac_bytes = bytes(int(p, 16) for p in mac.split(":"))
    ip_bytes = ipaddress.IPv4Address(ip).packed
    cab = struct.pack("!BBBBIHH", 1, 1, 6, tipo, XID, 0, 0x8000)
    return cab + mac_bytes + b"\x00" * 4 + ip_bytes + b"\x00" * 4 + mensagem.encode() + b"\x00" * 16


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))
    print(f"Servidor DHCP simulado em {HOST}:{PORT}")
    print(f"Pool disponivel: {POOL[0]} ate {POOL[-1]}\n")

    while True:
        dados, addr = sock.recvfrom(2048)
        tipo = dados[3]
        mac = dados[12:18].hex(":")
        rotulo = TIPO.get(tipo, "DESCONHECIDO")

        if tipo == 1:
            print(f"[{mac}] DISCOVER recebido")
            livre = next((ip for ip in POOL if ip not in ATRIBUIDOS.values()), None)
            if livre is None:
                print("[X] Pool esgotado")
                continue
            ATRIBUIDOS[mac] = livre
            print(f"[{mac}] OFFER enviada -> {livre}")
            sock.sendto(montar(2, mac, "0.0.0.0", "OFERTA"), addr)

        elif tipo == 3:
            ip = ATRIBUIDOS.get(mac, "0.0.0.0")
            print(f"[{mac}] REQUEST recebido -> confirmando {ip}")
            sock.sendto(montar(4, mac, ip, "CONFIRMADO"), addr)

        else:
            print(f"[{mac}] {rotulo} (ignorado)")


if __name__ == "__main__":
    main()
