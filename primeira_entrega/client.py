from datetime import datetime
import threading
import socket
import time

SERVER_IP = '127.0.0.1'
SERVER_PORT = 7777

def main():

    print("|-------------------- COMANDOS ----------------------|")
    print("| Para entrar na sala -> 'Olá, meu nome é <username>'|")
    print("| Para sair da sala -> 'bye'                         |")
    print("|____________________________________________________|")

    proceed = True
    while proceed == True: # Verificação para entrar no chat com o comando certo
        inital_msg = str(input())

        if inital_msg == "bye":
            exit()
        elif inital_msg.startswith("Olá, meu nome é") :
            proceed = False
            # obtem o nome do cliente
            msg = inital_msg.split()
            username = msg[-1]

            # conecta o cliente
            client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            server_address = (SERVER_IP, SERVER_PORT)
            print("Conectado")
            # Envie uma mensagem inicial para estabelecer a comunicação
            client.sendto(f"{username} entrou na sala\n".encode('utf-8'), server_address)

            # getsockname() retorne ip e porta do cliente para formatar o envio da mensagem
            client_ip, client_port = client.getsockname()

            # inicializa as threads
            thread1 = threading.Thread(target=receiveMessages, args=[client, username])
            thread2 = threading.Thread(target=sendMessages, args=[client, server_address, username, client_ip, client_port])
            thread1.start()
            thread2.start()
        else:
            print("|-------------------- COMANDOS ----------------------|")
            print("| Para entrar na sala -> 'Olá, meu nome é <username>'|")
            print("| Para sair da sala -> 'bye'                         |")
            print("|____________________________________________________|")

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
                print("Você saiu da sala")
                return
        except socket.error:
            time.sleep(0.1)

def sendMessages(client, server_address, username, client_ip, client_port):
    while True:
        msg = input('\n').strip()
        if msg.lower() == 'bye':
            print("Você saiu da sala")
            return
        timestamp = datetime.now().strftime('%H:%M:%S %Y-%m-%d')
        full_message = f'{client_ip}:{client_port}/~{username}: {msg} {timestamp}\n'
        
        with open('mensagem.txt', 'w') as file:
            file.write(full_message)
        
        sendFile(client, server_address, 'mensagem.txt')


if __name__ == "__main__":
    main()