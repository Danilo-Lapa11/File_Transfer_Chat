import threading
import socket

clients = []

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(('127.0.0.1', 7777))

    while True:
        data, addr = server.recvfrom(1024)
        clients.append(addr)

        thread = threading.Thread(target=messagesTreatment, args=(server, data, addr))
        thread.start()

def messagesTreatment(server, data, addr):
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
    clients.remove(addr)

if __name__ == "__main__":
    main()
