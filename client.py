from datetime import datetime
import threading
import socket
import time

SERVER_IP = '127.0.0.1'
SERVER_PORT = 7777

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = (SERVER_IP, SERVER_PORT)
    username = input('Username: ')
    
    print("Conectado")    
    print("Para sair da sala digite 'bye'")

    client.sendto(f"{username} entrou na sala".encode('utf-8'), server_address)

    thread1 = threading.Thread(target=receiveMessages, args=[client, username])
    thread2 = threading.Thread(target=sendMessages, args=[client, server_address, username])

    thread1.start()
    thread2.start()

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
        try:
            msg = input('\n').strip()
            timestamp = datetime.now().strftime('%H:%M:%S %Y-%m-%d')
            full_message = f'{server_address[0]}:{server_address[1]}/~{username}: {msg} {timestamp}'
            client.sendto(full_message.encode('utf-8'), server_address)

            if msg.lower() == 'bye':
                client.sendto(f"/exit {username}".encode('utf-8'), server_address)
                print("You left the room.")
                return

        except:
            return

if __name__ == "__main__":
    main()
