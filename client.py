from datetime import datetime
import threading
import socket
import time

SERVER_IP = '127.0.0.1'
SERVER_PORT = 7777

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = (SERVER_IP, SERVER_PORT)
    username = input('Olá, meu nome é: ')
    
    print("Conectado")    
    print("Para sair da sala digite 'bye'")

    client.sendto(f"{username} entrou na sala\n".encode('utf-8'), server_address)

    thread1 = threading.Thread(target=receiveMessages, args=[client, username])
    thread2 = threading.Thread(target=sendMessages, args=[client, server_address, username])

    thread1.start()
    thread2.start()


def sendFile(client, server_address, filepath):
    with open(filepath, 'rb') as file:
        chunk = file.read(1024)
        
        while chunk: # enquanto houver bytes fragmentados ele lê e envia o fragmento até 1024 bytes
            client.sendto(chunk, server_address)
            chunk = file.read(1024)


def receiveMessages(client, username):
    while True:
        try:
            msg = client.recv(1024).decode('utf-8')
            print(msg + '\n')
            if "/~" + username + ": bye" in msg:
                print("You left the room.")
                return
        except socket.error:
            time.sleep(0.1)

def sendMessages(client, server_address, username):
    while True:
        msg = input('\n').strip()
        if msg.lower() == 'bye':
            print("You left the room.")
            return
        timestamp = datetime.now().strftime('%H:%M:%S %Y-%m-%d')
        full_message = f'{server_address[0]}:{server_address[1]}/~{username}: {msg} {timestamp}\n'
        
        with open('mensagem.txt', 'w') as file:
            file.write(full_message)
        
        sendFile(client, server_address, 'mensagem.txt')


if __name__ == "__main__":
    main()
