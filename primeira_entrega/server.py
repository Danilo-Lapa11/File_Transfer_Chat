
def main():
    # Conexão do Servidor
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((SERVER_IP, SERVER_PORT))

    while True:
        data, addr = server.recvfrom(1024) # buffer de 1024 bytes
        if addr not in clients:
            clients.append(addr) # add o cliente novo na lista de clientes conectados
            
        thread = threading.Thread(target=messagesTreatment, args=(server, data, addr))
        thread.start()


def messagesTreatment(server, data, addr):
    # Só entra quando for a primeira mensagem após o comando de entrar na sala
    if data.endswith(b"entrou na sala"):    
        # Inicializa a fila para o cliente, caso ele não esteja no dicionário
        if addr not in message_queues:
            message_queues[addr] = []

    # Entra se o comando bye for acionado no client
    elif data.endswith(b"saiu da sala"):
        deleteClient(addr)

    # Tratamento de mensagens  
    else:
        eof = data[:10].decode('utf-8').strip('\0') == 'True'
        content = data[10:]  # Remove os metadados do conteúdo

        # Adiciona o fragmento atual à fila do cliente
        message_queues[addr].append(content)

        if eof: # Se for o último fragmento, reconstrua e processe a mensagem
            message = b''.join(message_queues[addr]) # união da fila de fragmentos para formar a mensagem completa
            print(f"~ Server <Reconstrução do arquivo enviado para {addr} - concluída>\nTransmitindo mensagem")

            broadcast(server, message, addr) 
            message_queues[addr].clear() # Limpa a fila após o processamento


def broadcast(server, data, addr):
    for clientAddr in clients:
        if clientAddr != addr:
            server.sendto(data, clientAddr)


def deleteClient(addr):
    if addr in clients:
        clients.remove(addr) # remove o cliente da lista de clientes conectados
        message_queues.pop(addr) #remove o cliente do dicionário de fila de mensagens
        print(f"~ Server <Cliente {addr} removido>") # informa no server que o usario foi removido


import threading
import socket

SERVER_IP = '127.0.0.1'
SERVER_PORT = 7777

# Lista de Clientes 
clients = []
# Dicionário para armazenar as filas de fragmentos de cada cliente
global message_queues
message_queues = {}

if __name__ == "__main__":
    main()

