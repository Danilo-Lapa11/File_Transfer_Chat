# File Transfer Chat - *Chat de Transferência de Arquivo*

Neste projeto consistirá em duas partes de desenvolvimento de um chat de transferência de arquivos, na primeira parte implementaremos um chat de transmissão de arquivos com UDP e na segunda parte implementaremos transferência confiável RDT 3.0 no chat.

## **1° Entrega:** Transmissão com UDP

### Descrição
Na primeira parte é implementado um sistema de chat básico usando o protocolo UDP. Ele consiste em um servidor (`server.py`) e um cliente (`client.py`). Os usuários podem se conectar ao servidor e enviar mensagens de texto para todos os outros usuários conectados demonstrando a utilização de sockets usando o protocolo UDP, threads e manipulação de arquivos txt em Python como forma de mensagens.

## Funcionalidades
- Conexão de múltiplos clientes ao servidor.
- Envio de mensagens em tempo real.
- Fragmentação e reconstrução de mensagens para garantir a integridade da transmissão.
- Comandos para entrar e sair do chat.
- Vizualização da fragmentação e resconstrução de cada fragmento.

## **2° Entrega:** Transmissão confiável com RDT 3.0

### Descrição
Na segunda parte é implementado o protocolo de transferência confiável RDT 3.0 que utiliza de mensagem ACK para informar que ao lado transmissor que a mensagem chegou juntamente com a implementação de um checksum sobre os dados a fim de verificar a integridade da mensagem visto que o protocolo UDP é sucetível a perdas de pacotes e corrupção de bits da mensagem enviada.

![image](https://github.com/Danilo-Lapa11/File_Transfer_Chat/assets/123251524/18f3ba9d-1127-459d-ad42-b61b7e3e17ce) 
![image](https://github.com/Danilo-Lapa11/File_Transfer_Chat/assets/123251524/fb6d9682-c7b5-4cf8-8202-75d47c7d075a)
*Referências: 8th Edição - 2021, Redes de computadores e a Internet, James F. Kurose (Autor), Keith W. Ross (Autor)*

A aplicação funciona como um chat multithread e para implementar o RDT 3.0 nessa aplicação foi assumido que o tanto o cliente quanto o servidor atuam como trasmissor e receptor nessa aplicação. Assim, a ideia principal do protocolo RDT 3.0 na aplicação consiste em: 

#### Lado Cliente

- O cliente envia uma mensagem se essa mensagem for maior que buffer e precisar ser fragmentada ela vai ser fragmentada e enviado cada fragmento ao servidor. Irá setar um timer para o envio, assumindo que se o pacote for perdido ou corrompido o servidor vai descartar o pacote. Se o pacote for recebido com sucesso o timer deve ser desligado. Se não for recebido e o timer acabar o cliente deve reenviar o mesmo pacote de novo.

#### Lado Servidor

- Já o servidor ao receber um fragmento deve verificar o checksum do fragmento e o numero de sequência, se houver erro no checksum ou o numero de sequência errado, só aguarda. Caso as duas verificações deem certo, o servidor deve setar um timer enviar o pacote aos clientes um por vez por broadcast e aguardar o ACK do cliente de cada pacote recebido informando que o pacote chegou, o servidor vai ter que esperar o recebimento do ACK do pacote enviado, para depois enviar o pacote para outro cliente, a fim de manter a integridade do envio. Ou seja, o servidor seta o timer e o numero de sequência inicial como 0, envia para o primeiro cliente por try, e espera o recebimento do ack do cliente desse pacote se o except do timer for acionado deve reenviar o pacote para a msm pessoa. Quando o servidor receber com sucesso o ack do cliente ele repete o processo enviando para a proxima pessoa o mesmo fragmento.

## Funcionalidades
### Implementadas com Sucesso
- Funcionalidades da primeira entrega corrigidas e refatoradas
- Comando de entrar na sala via Three-Way Handshake
- Vizualização de Conexão dos clientes no terminal do servidor
- Vizualização de erros de timeout e  
- SYN ACK e ACK do Three-Way Handshake
- Checksum

### Implementadas com Erros - Melhorias Futuras
- Manipulação dos ACK - Erro de paralalismo nas funções Thread
- Testes com timouts referente as Threads de envio e recebimento das mensagens
- Comando de saída da sala - Implemetação igual ao da primeira entrega, sem ACK devido aos erros acima.

## Requisitos
- Python 3.10.7 ou outra versão

## Instalação
Não é necessária uma instalação específica, mas é preciso ter o Python 3 instalado no sistema. 

O projeto pode ser baixado diretamente do repositório.

```
git clone https://github.com/Danilo-Lapa11/File_Transfer_Chat.git
```

## Uso
**Para iniciar o servidor:**

```
python server.py
```

**Para iniciar o cliente:**

```
python client.py
```
