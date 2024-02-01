import threading
import socket

SERVER_IP = '127.0.0.1'
SERVER_PORT = 7777

clients = []

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
    # Adiciona um identificador único para cada cliente usando a porta que ele entrou 
    filename = f'{addr[1]}.txt'
    
    with open(filename, 'ab') as file:
        file.write(data)
        print(f"Fragmento recebido de {addr}")

    with open(filename, 'r') as file:
        message = file.read()
        if '\n' in message:  # Indica o fim da mensagem
            print(f"Reconstrução do arquivo de {addr} - CONCLUÍDA")
            broadcast(server, message.encode('utf-8'), addr)
            print("Mensagem enviada")
            open(filename, 'w').close()  # Limpa o arquivo


def broadcast(server, data, addr):
    for clientAddr in clients:
        if clientAddr != addr:
            try:
                server.sendto(data, clientAddr)
            except socket.error:
                deleteClient(clientAddr)

def deleteClient(addr):
    if addr in clients:
        clients.remove(addr)

if __name__ == "__main__":
    main()
