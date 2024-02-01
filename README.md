# File Transfer Chat - *Chat de Transferência de Arquivo*

Neste projeto consistirá em duas partes de desenvolvimento de um chat de transferência de arquivos, na primeira parte implementaremos uma transmissão de arquivos com UDP e na segunda parte implementaremos um chat com transferência confiável RDT 3.0.

## **Parte 1:** Transmissão com UDP

### Descrição
Na primeira parte é implementado um sistema de chat básico usando o protocolo UDP. Ele consiste em um servidor (`server.py`) e um cliente (`client.py`). Os usuários podem se conectar ao servidor e enviar mensagens de texto para todos os outros usuários conectados demonstrando a utilização de sockets usando o protocolo UDP, threads e manipulação de arquivos txt em Python como forma de mensagens.

## Funcionalidades
- Conexão de múltiplos clientes ao servidor.
- Envio de mensagens em tempo real.
- Fragmentação e reconstrução de mensagens para garantir a integridade da transmissão.
- Comandos para entrar e sair do chat.
- Vizualização do fragmentação e resconstrução de cada fragmento

## **Parte 2:** Transmissão confiável com RDT 3.0
Em andamento...


## Requisitos
- Python 3.10.7 ou outra versão

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

