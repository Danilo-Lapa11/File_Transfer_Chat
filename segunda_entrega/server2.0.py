
def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    print("Servidor iniciado e aguardando conexões...\n")

    while True:
        data, client_address = server_socket.recvfrom(1024)
        
        # Inicia uma nova thread para lidar com a mensagem recebida
        thread = threading.Thread(target=handle_client, args=(server_socket, data, client_address))
        thread.start()
    
def send_ack_handshake(server_socket, client_address, username):
    ack_message = f"ACK:{username}".encode('utf-8')
    server_socket.sendto(ack_message, client_address)
    print('~ Server <SYN ACK enviado>')

def handle_client(server_socket, data, client_address):
    if data.startswith(b"SYN:"):
        # Extração do username a partir da mensagem SYN
        username = data.decode('utf-8').split(":")[1]
        print(f"~ from Client <SYN ACK recebido de {username}>")
        send_ack_handshake(server_socket, client_address, username)

    elif data.endswith(b"entrou na sala"):
        print(f"~ Server <Conexão estabelecida>\n")
        clients.append(client_address)  # Adiciona o cliente à lista de clientes conectados
        expected_seq_nums[client_address] = 0

        # envia para todos que o usuario entoru na sala
        for clientAddr in clients:
            if clientAddr != client_address:
                server_socket.sendto(data, clientAddr)
    
    else:
        # Tratamento de mensagens regulares do chat
        messagesTreatment(server_socket, data, client_address)


def messagesTreatment(server, data, addr):

    eof = data[0]                                          # Flag eof (informa se é o ultimo fragmento)
    checksum_received = data[1:5]                          # Checksum (Verifica se houve erros de corrupção de mensagem)
    seq_num_received = int.from_bytes(data[5:6], 'big')    # Número de sequencia do pacote recebido em int  
    message = data[6:]                                     # Mensagem

    # Calcula o checksum do pacote recebido
    checksum_calculated = get_checksum(message)
        
    # Verifica o checksum e o número de sequência
    if (checksum_received == checksum_calculated) and (seq_num_received == expected_seq_nums[addr]):
        
        # ENVIA ACK PRO CLIENTE
        seq_num = seq_num_received.to_bytes(1, 'big')
        send_ack(server, addr, seq_num)

        if eof == 1: # ultimo fragmento
            # Processa a mensagem completa
            broadcast(data, server, addr)  # Envia a mensagem para todos
            print(f"Mensagem completa recebida de {addr}")
            expected_seq_nums[addr] = 0
        else:
            broadcast(server, addr)  # Envia a mensagem para todos
    else:
        print(f"~Server <Erro de checksum ou sequência incorreta> de {addr}")


def broadcast(package ,server, addr):
    # Envia o fragmento com cabeçalho para cada cliente, exceto o remetente
    for clientAddr in clients:
        if clientAddr != addr:
            server.sendto(package, clientAddr)
    print(f"~ Server(Broadcast): <Mensagem enviada>")


def send_ack(server, addr, seq_num):
    ack_packet = b'ACK' + seq_num
    server.sendto(ack_packet, addr)


def get_checksum(data):
    checksum_value = 0
    for i in range(0, len(data), 2):
        if i + 1 < len(data):
            word = (data[i] << 8) + data[i + 1]
            checksum_value += word
            while (checksum_value >> 16) > 0:
                checksum_value = (checksum_value & 0xFFFF) + (checksum_value >> 16)
    checksum_value = ~checksum_value & 0xFFFF
    return checksum_value.to_bytes(4, 'big')


def deleteClient(addr):
    if addr in clients:
        clients.remove(addr) # remove o cliente da lista de clientes conectados
        expected_seq_nums.pop(addr) #remove o cliente do dicionário de fila de mensagens
        print(f"~ Server: <Cliente {addr} removido>") # informa no server que o usario foi removido


import threading
import socket # Sockets

SERVER_IP = '127.0.0.1'
SERVER_PORT = 7777



# Lista de Clientes Conectados
clients = []
# Dicionário para armazenar as filas de fragmentos de cada cliente

expected_seq_nums = {}

if __name__ == "__main__":
    main()
