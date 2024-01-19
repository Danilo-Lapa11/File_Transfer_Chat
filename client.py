from datetime import datetime
import threading
import socket
import time

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = ('127.0.0.1', 7777)
    username = input('Username: ')
    
    thread1 = threading.Thread(target=receiveMessages, args=[client])
    thread2 = threading.Thread(target=sendMessages, args=[client, server_address, username])

    thread1.start()
    thread2.start()

def receiveMessages(client):
    while True:
        try:
            msg = client.recv(1024).decode('utf-8')
            print(msg + '\n')
        except socket.error:
            time.sleep(0.1)

def sendMessages(client, server_address, username):
    while True:
        try:
            msg = input('\n').strip()
            timestamp = datetime.now().strftime('%H:%M:%S %Y-%m-%d')
            full_message = f'{server_address[0]}:{server_address[1]}/~{username}: {msg} {timestamp}'
            client.sendto(full_message.encode('utf-8'), server_address)
        except:
            return

if __name__ == "__main__":
    main()
