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
    message = data.decode('utf-8')
    if message.startswith("/exit"):
        deleteClient(addr)
    else:
        try:
            broadcast(server, data, addr)
        except:
            deleteClient(addr)

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
