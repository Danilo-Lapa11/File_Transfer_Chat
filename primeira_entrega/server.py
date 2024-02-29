def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((SERVER_IP, SERVER_PORT))

    while True:
        data, addr = server.recvfrom(1024)
        if addr not in clients:
            clients.append(addr)
            
        thread = threading.Thread(target=messagesTreatment, args=(server, data, addr))
        thread.start()


def messagesTreatment(server, data, addr):
    eof = data[:10].decode('utf-8').strip('\0') == 'True'
    content = data[10:]  # Remove os metadados do conteúdo

    # Inicializa a fila para o cliente, se não ele cria a fila vazia
    if addr not in message_queues:
        message_queues[addr] = []

    # Adiciona o fragmento atual à fila do cliente
    message_queues[addr].append(content)

    if eof: # Se for o último fragmento, reconstrua e processe a mensagem
        message = b''.join(message_queues[addr]) # união da fila de fragmentos para formar a mensagem completa
        print(f"~ Server <Reconstrução do arquivo enviado para {addr} - concluída>\nTransmitindo mensagem")

        broadcast(server, message, addr) 
        del message_queues[addr] # Limpa a fila após o processamento

def broadcast(server, data, addr):
    for clientAddr in clients:
        if clientAddr != addr:
            try:
                server.sendto(data, clientAddr)
            except:
                deleteClient(clientAddr)

def deleteClient(addr):
    if addr in clients:
        clients.remove(addr)
        print(f"~ Server <Cliente {addr} removido>")

import threading
import socket

SERVER_IP = '127.0.0.1'
SERVER_PORT = 7777

# Lista de Clientes 
clients = []
# Dicionário para armazenar as filas de fragmentos de cada cliente
message_queues = {}

if __name__ == "__main__":
    main()