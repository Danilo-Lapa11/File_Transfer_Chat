
def main():
    print("|-------------------- COMANDOS ----------------------|")
    print("| Para entrar na sala -> 'Olá, meu nome é <username>'|")
    print("| Para sair da sala -> 'bye'                         |")
    print("|____________________________________________________|")

    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (SERVER_IP, SERVER_PORT)

    while True:  # Verificação para entrar no chat com o comando
        initial_msg = input()
        # Proibe que a mensagem seja diferente do comando e que haja um usuário com string vazia
        if (initial_msg.lower().startswith("olá, meu nome é")) and (initial_msg.split(" ")[-1] != ''):
            username = initial_msg.split(" ")[-1]

            if handshake(client, server_address, username):

                # Passo 3: Cliente envia confirmação de conexão
                confirm_message = f"{username} entrou na sala".encode('utf-8')
                client.sendto(confirm_message, server_address)
                print('Conectado')
                # getsockname() retorna ip e porta do cliente para formatar o envio da mensagem
                client_ip, client_port = client.getsockname()
                # Evento que sincroniza o fechamento das threads
                close_event = Event()

                thread1 = Thread(target=sendMessages, args=(client, server_address, username, client_ip, client_port, close_event))
                thread2 = Thread(target=receiveMessages, args=(client, server_address, close_event))
                thread1.start()
                thread2.start()
                break
            else:
                client.close()  # Fecha o socket se a conexão não for estabelecida
                return
        else:
            print("<Comando inválido> Tente novamente 'Olá, meu nome é <username>'")


# Three-way Handshake
def handshake(client_socket, server_address, username):
    # Passo 1: Cliente envia SYN
    syn_message = f"SYN:{username}".encode('utf-8')
    client_socket.sendto(syn_message, server_address)
    
    # Espera pela resposta ACK do servidor
    try:

        # FALTA DEFINIR TIMEOUT
        # client_socket.settimeout(5)  # Define um timeout


        ack, _ = client_socket.recvfrom(1024)
        if ack.startswith(b"ACK"):
            # Passo 3: Cliente envia confirmação de conexão
            client_socket.settimeout(None)  # Remove o timeout
            print("Conexão estabelecida com sucesso.")
            return True
    except socket.timeout:
        print("Não foi possível estabelecer a conexão. Timeout.")
        return False


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


def send_ack(client, server_address, seq_num):
    ack_packet = b'ACK' + seq_num
    client.sendto(ack_packet, server_address)


def sendMessages(client, server_address, username, client_ip, client_port, close_event):
    seq_num = 0  # Número de sequência inicial
    ack_expected = False  # Flag para indicar se um ACK é esperado

    while True:
        msg = input('\n').strip()
        if msg.lower() == 'bye':
            print("Você saiu da sala.")
            client.sendto(f"{username} saiu da sala".encode('utf-8'), server_address)
            close_event.set()
            break
        else:
            # Formatação da mensagem
            timestamp = datetime.now().strftime('%H:%M:%S %Y-%m-%d')
            full_message = f'{client_ip}:{client_port}/~{username}: {msg} {timestamp}'

            with open('mensagem.txt', 'w') as file:
                file.write(full_message)
            
            with open('mensagem.txt', 'rb') as file:
                chunk = file.read(1018)  # Considera espaço para EOF, checksum e número de sequência

                while chunk:
                    eof = 1 if len(chunk) < 1018 else 0
                    checksum = get_checksum(chunk)
                    header = eof.to_bytes(1, 'big') + checksum.to_bytes(4, 'big') + seq_num.to_bytes(1, 'big')
                    packet = header + chunk
                    
                    while True:
                        try:
                            # Define um timeout para esperar por ACKs
                            #client.settimeout(3)  
                            # Tenta enviar fragmento
                            client.sendto(packet, server_address)

                            # Tenta receber ACK
                            # Aguarda o ACK após o envio de cada fragmento
                            while ack_expected:
                                ack, _ = client.recvfrom(1024)
                                ack = ack.decode('utf-8')
                                if ack == f"ACK{seq_num}":
                                    ack_expected = False  # ACK recebido, pode prosseguir para o próximo fragmento
                                    break
                                else:
                                    time.sleep(2)
                        
                        except socket.timeout:
                            print("Timeout, retransmitindo...")
                            continue  # Continua no loop para retransmitir

                        chunk = file.read(1018)  # Lê o próximo fragmento
                        seq_num = 1 - seq_num  # Alterna o número de sequência


def receiveMessages(client, server_address, close_event):
    queue_fragments = []
    last_seq_num = None  # Rastreia o último número de sequência recebido

    while not close_event.is_set():  # Verifica se o evento de fechar cliente foi sinalizado
        try:
            data = client.recv(1024)
            
            # Ignora mensagens de controle (entrar e sair da sala)
            if data.endswith(b'entrou na sala'):
                print(data.decode('utf-8') + '\n')
            elif data.endswith(b'saiu da sala'):
                print(data.decode('utf-8') + '\n')
            elif data.startswith(b'ACK'):
                pass
            else:   

                eof = data[0] == 1
                checksum_received = int.from_bytes(data[1:5], byteorder='big')
                seq_num_received = data[5:6]
                fragment = data[6:]

                checksum_calculated = get_checksum(fragment)

                # # Envia ACK para cada pacote recebido
                # send_ack(client, server_address, seq_num_received)

                # Verifica checksum e se o pacote é um novo fragmento
                if checksum_received == checksum_calculated and seq_num_received != last_seq_num:
                    queue_fragments.append(fragment.decode('iso-8859-1'))
                    last_seq_num = seq_num_received  # Atualiza o último número de sequência recebido
                    
                    # Se é o fim da mensagem, imprime a mensagem completa e limpa a fila
                    if eof:
                        full_message = ''.join(queue_fragments)
                        print(full_message + '\n')
                        queue_fragments.clear()
                else:
                    print("cliente - erro de checksum detectado ou fragmento duplicado. ACK enviado.")
                    
        except OSError:
            break


from datetime import datetime
from threading import Thread, Event
import socket
import time

SERVER_IP = '127.0.0.1'
SERVER_PORT = 7777

if __name__ == "__main__":
    main()
