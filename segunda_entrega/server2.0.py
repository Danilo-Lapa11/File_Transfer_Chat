
def main():
    # Conexão do Servidor
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((SERVER_IP, SERVER_PORT))

    while True:
        # Recebe dados dos clientes - Buffer de 1024 bytes
        data, addr = server.recvfrom(1024)

        # Verifica se é um novo cliente. Se for, adiciona no servidor
        if addr not in clients and addr not in message_queues:
                clients.append(addr) 
                message_queues[addr] = []

        # Comando de entrada da sala - informa para todos os conectados que o novo cliente entrou na sala        
        if data.endswith(b'entrou na sala'):
            for clientAddr in clients:
                if clientAddr != addr:
                    server.sendto(data, clientAddr)

        # Comando de saída da sala - informa para todos os conectados que o cliente saiu na sala
        elif data.endswith(b'saiu da sala'):
            for clientAddr in clients:
                if clientAddr != addr:
                    server.sendto(data, clientAddr)
            deleteClient(addr)

        else: 
            # Inicia as threads de mensagens
            thread = threading.Thread(target=messagesTreatment, args=(server, data, addr))
            thread.start()


def messagesTreatment(server, data, addr):
    # Separa o fragmento em: 
    #       Flag eof (informa se é o ultimo fragmento)
    #       Checksum (Verifica se houve erros de corrupção de mensagem)
    #       Fragmento (Mensagem)

    eof = data[0] 
    checksum_received = data[1:5]
    fragment = data[5:]

    # Usa a biblioteca para calcular o checksum do fragmento
    checksum_calculated = zlib.crc32(fragment)
    
    # Faz a comparação com o checksum que veio no pacote com o checksum calculado novamente para ver se não houve erros
    if checksum_received == checksum_calculated.to_bytes(4, 'big'):

        # Verifica se é o ultimo fragmento
        if eof == 1:
            message_queues[addr].append(fragment)
            # Processa o final da mensagem
            print(f"Mensagem completa recebida de {addr}")

            broadcast(server, addr) # Envia a mensagem pra todos
            message_queues[addr].clear() # Limpa a fila depois da mensagem ter sido enviada
        else:
            message_queues[addr].append(fragment)
    else:
        print("server - Erro de checksum. Mensagem pode estar corrompida.")
        # reenvia

def broadcast(server, addr):
    mensagem_completa = b''.join(message_queues[addr])
    
    # Inicia a fragmentação da mensagem e a preparação para envio
    inicio = 0
    tamanho_mensagem = len(mensagem_completa)

    while inicio < tamanho_mensagem:
        # Determina o final do fragmento, considerando o limite de 1024 bytes
        fim = min(inicio + 1024 - 5, tamanho_mensagem)  # Reserva 5 bytes para checksum e EOF
        fragmento = mensagem_completa[inicio:fim]
        
        # Calcula o checksum do fragmento
        checksum = zlib.crc32(fragmento)

        # Determina se este é o último fragmento
        eof = 1 if fim == tamanho_mensagem else 0
        
        # Prepara o cabeçalho com checksum e EOF
        cabeçalho = eof.to_bytes(1, byteorder='big') + checksum.to_bytes(4, byteorder='big')
        
        # Envia o fragmento com cabeçalho para cada cliente, exceto o remetente
        for clientAddr in clients:
            if clientAddr != addr:
                server.sendto(cabeçalho + fragmento, clientAddr)
        
        inicio += 1024 - 5  # Atualiza o início para o próximo fragmento

    print(f"~ Server(Broadcast): <Mensagem enviada>")



def deleteClient(addr):
    if addr in clients:
        clients.remove(addr) # remove o cliente da lista de clientes conectados
        message_queues.pop(addr) #remove o cliente do dicionário de fila de mensagens
        print(f"~ Server: <Cliente {addr} removido>") # informa no server que o usario foi removido


import threading
import socket # Sockets
import zlib # Checksum - CRC32

SERVER_IP = '127.0.0.1'
SERVER_PORT = 7777

# Lista de Clientes Conectados
clients = []
# Dicionário para armazenar as filas de fragmentos de cada cliente
message_queues = {}

if __name__ == "__main__":
    main()

