import socket
import struct

ALVO = "127.0.0.1"
PORTA = 5000

PROTOCOLOS = {6: "TCP", 17: "UDP", 1: "ICMP"}


def abrir_conexao():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    s.connect((ALVO, PORTA))
    return s


def ler_pacote_bruto():
    s = abrir_conexao()
    s.sendall(b"GET / HTTP/1.1\r\nHost: x\r\n\r\n")
    bruto = s.recv(1024)
    s.close()
    return bruto


def mostrar_tcp(raw):
    print("=== ESTRUTURA DO PACOTE TCP ===")

    ip_ver_ihl = raw[0]
    versao = ip_ver_ihl >> 4
    ihl = (ip_ver_ihl & 0x0F) * 4

    print(f"IP versao ........ {versao}")
    print(f"IP tamanho header  {ihl} bytes")
    print(f"IP tamanho total . {struct.unpack('!H', raw[2:4])[0]} bytes")

    protocolo = raw[9]
    print(f"IP protocolo ...... {protocolo} ({PROTOCOLOS.get(protocolo, 'desconhecido')})")

    ip_origem = socket.inet_ntoa(raw[12:16])
    ip_destino = socket.inet_ntoa(raw[16:20])
    print(f"IP origem ......... {ip_origem}")
    print(f"IP destino ........ {ip_destino}")

    tcp = raw[ihl:]
    porta_origem, porta_destino = struct.unpack("!HH", tcp[0:4])
    print(f"TCP porta origem .. {porta_origem}")
    print(f"TCP porta destino . {porta_destino}")
    print(f"TCP seq ........... {struct.unpack('!I', tcp[4:8])[0]}")
    print(f"TCP ack ........... {struct.unpack('!I', tcp[8:12])[0]}")

    flags = tcp[13]
    nomes = []
    for bit, nome in [(0x02, "SYN"), (0x10, "ACK"), (0x01, "FIN"), (0x08, "PSH"), (0x04, "RST")]:
        if flags & bit:
            nomes.append(nome)
    print(f"TCP flags ......... {flags:08b} -> {', '.join(nomes) if nomes else 'sem flags'}")


def mostrar_payload(raw):
    print("\n=== PAYLOAD (dados da aplicacao) ===")
    idx = raw.find(b"\r\n\r\n")
    if idx != -1:
        print(raw[idx + 4:].decode("utf-8", errors="ignore"))


if __name__ == "__main__":
    pacote = ler_pacote_bruto()
    mostrar_tcp(pacote)
    mostrar_payload(pacote)
