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
Este projeto implementa um sistema de chat básico com transferência confiável, utilizando o canal de transmissão confiável rdt3.0. O sistema permite que os clientes entrem e saiam da sala, enviem mensagens para todos os participantes e recebam mensagens de outros clientes.

## Requisitos
- Python 3.10.7 ou outra versão
- Biblioteca zlib (já incluída na maioria das instalações Python)
- Acesso à biblioteca de sockets do Python

## Instalação
Não é necessária uma instalação específica, mas é preciso ter o Python 3 instalado no sistema. O projeto pode ser baixado diretamente do repositório.

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

