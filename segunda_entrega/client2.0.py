
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

            # Cria um evento para sincronizar o encerramento
            close_event = Event()

            # Passa o evento como argumento para as threads
            thread1 = threading.Thread(target=receiveMessages, args=[client, close_event])
            thread2 = threading.Thread(target=sendMessages, args=[client, server_address, username, client_ip, client_port, close_event])

            thread2.start()
            thread1.start()
        else:
            # Repete a mensagem de comandos e o input caso não tenha digitado o comando de entrar na sala
            print("|-------------------- COMANDOS ----------------------|")
            print("| Para entrar na sala -> 'Olá, meu nome é <username>'|")
            print("| Para sair da sala -> 'bye'                         |")
            print("|____________________________________________________|")


def get_checksum(data):
    checksum_value = 0
    for i in range(0, len(data), 2):
        if i + 1 < len(data):
            word = (data[i] << 8) + data[i + 1]
            checksum_value += word
            while (checksum_value >> 16) > 0:
                checksum_value = (checksum_value & 0xFFFF) + (checksum_value >> 16)
    checksum_value = ~checksum_value & 0xFFFF
    return checksum_value


def receiveMessages(client, close_event):

    while not close_event.is_set():  # Verifica se o evento de fechar cliente foi sinalizado
        try:
            queue_fragments = []
            while True:
                data = client.recv(1024)
                
                if data.endswith(b'entrou na sala'):
                    print(data.decode('utf-8') + '\n')

                elif data.endswith(b'saiu da sala'):
                    print(data.decode('utf-8') + '\n')
                    
                else:
                    if not data:
                        break  # Encerra o loop se nenhum dado for recebido (socket fechado)

                    eof = data[0] == 1  # Considera 1 como True e 0 como False para EOF
                    checksum_received = int.from_bytes(data[1:5], byteorder='big')
                    fragment = data[5:]  # Correção: extrai o fragmento corretamente

                    checksum_calculated = get_checksum(fragment)

                    if checksum_received == checksum_calculated:
                        queue_fragments.append(fragment.decode('iso-8859-1'))  # Decodifica e adiciona à fila
                        if eof:
                            full_message = ''.join(queue_fragments)
                            print(full_message + '\n')
                            queue_fragments.clear()
                    else:
                        
                        print("cliente - erro de checksum detectado. Fragmento descartado.")
        except OSError:
            break

    queue_fragments = []
    while True:
        data = client.recv(1024)
        
        if data.endswith(b'entrou na sala'):
            print(data.decode('utf-8') + '\n')

        elif data.endswith(b'saiu da sala'):
            print(data.decode('utf-8') + '\n')
            
        else:
            if not data:
                break  # Encerra o loop se nenhum dado for recebido (socket fechado)

            eof = data[0] == 1  # Considera 1 como True e 0 como False para EOF
            checksum_received = int.from_bytes(data[1:5], byteorder='big')
            fragment = data[5:]  # Correção: extrai o fragmento corretamente

            checksum_calculated = get_checksum(fragment)

            if checksum_received == checksum_calculated:
                queue_fragments.append(fragment.decode('iso-8859-1'))  # Decodifica e adiciona à fila
                if eof:
                    full_message = ''.join(queue_fragments)
                    print(full_message + '\n')
                    queue_fragments.clear()
            else:
                
                print("cliente - erro de checksum detectado. Fragmento descartado.")

            

def sendMessages(client, server_address, username, client_ip, client_port, close_event):
    while True:
        msg = input('\n').strip()
        if msg.lower() == 'bye':
            print("Você saiu da sala.")
            client.sendto(f"{username} saiu da sala".encode('utf-8'), server_address)
            close_event.set()  # Sinaliza para a outra thread encerrar
            break
        else:
            timestamp = datetime.now().strftime('%H:%M:%S %Y-%m-%d')
            full_message = f'{client_ip}:{client_port}/~{username}: {msg} {timestamp}'
            
            with open('mensagem.txt', 'w') as file1:
                file1.write(full_message)
                
            with open('mensagem.txt', 'rb') as file:
                chunk = file.read(1019)  # Reserva espaço para EOF e checksum
                while chunk:
                    eof = len(chunk) < 1019
                    checksum = get_checksum(chunk)
                    # Cabeçalho = 'flag eof' (1 byte) + 'checksum CRC32' (4 bytes)
                    header = (1 if eof else 0).to_bytes(1, 'big') + checksum.to_bytes(4, 'big')
                    client.sendto(header + chunk, server_address)
                    chunk = file.read(1019)



from datetime import datetime
import threading
import socket
from threading import Event

SERVER_IP = '127.0.0.1'
SERVER_PORT = 7777

if __name__ == "__main__":
    main()
