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

        if inital_msg.startswith("Olá, meu nome é") :
            proceed = False
            # obtem o nome do cliente
            msg = inital_msg.split()
            username = msg[-1] # pega o nome digitado pelo cliente

            # conecta o cliente
            client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            server_address = (SERVER_IP, SERVER_PORT)
            print("Conectado")

            # Envie uma mensagem inicial para estabelecer a comunicação
            client.sendto(f"{username} entrou na sala".encode('utf-8'), server_address)

            # getsockname() retorna ip e porta do cliente para formatar o envio da mensagem
            client_ip, client_port = client.getsockname()

            # inicializa as threads
            thread1 = threading.Thread(target=receiveMessages, args=[client, username])
            thread2 = threading.Thread(target=sendMessages, args=[client, server_address, username, client_ip, client_port])
            thread1.start()
            thread2.start()
        else:
            # Repete a mensagem de comandos e o input caso não tenha digitado o comando de entrar na sala
            print("|-------------------- COMANDOS ----------------------|")
            print("| Para entrar na sala -> 'Olá, meu nome é <username>'|")
            print("| Para sair da sala -> 'bye'                         |")
            print("|____________________________________________________|")

def sendFile(client, server_address, filepath):
    with open(filepath, 'rb') as file:
        total_sent = 0
        chunk = file.read(1024 - 10)  # Deixe espaço para metadados
        while chunk:
            eof = len(chunk) < (1024 - 10)
            header = f"{eof}".encode('utf-8').ljust(10, b'\0')  # Cabeçalho de 10 bytes
            client.sendto(header + chunk, server_address)
            total_sent += 1
            chunk = file.read(1024 - 10)


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
            print("Você saiu da sala.")
            client.sendto(f"{username} saiu da sala".encode('utf-8'), server_address)
            client.close()  # Fecha o socket antes de sair
            return  # Retorna para terminar a thread e não fecha o programa inteiro
        
        else: # 
            timestamp = datetime.now().strftime('%H:%M:%S %Y-%m-%d')
            full_message = f'{client_ip}:{client_port}/~{username}: {msg} {timestamp}\n' 
            with open('mensagem.txt', 'w') as file:
                file.write(full_message)
            
            sendFile(client, server_address, 'mensagem.txt')


from datetime import datetime
import threading
import socket
import time

SERVER_IP = '127.0.0.1'
SERVER_PORT = 7777

if __name__ == "__main__":
    main()
