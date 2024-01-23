def escrever_em_arquivo(mensagem, nome_arquivo):
    try:
        # Abre o arquivo em modo de escrita
        with open(nome_arquivo, 'w') as arquivo:
            # Escreve a mensagem no arquivo
            arquivo.write(mensagem)
        print(f'Mensagem escrita em {nome_arquivo} com sucesso.')
    except Exception as e:
        print(f'Ocorreu um erro: {e}')


def ler_e_imprimir_arquivo(nome_arquivo):
    try:
        # Abre o arquivo em modo de leitura
        with open(nome_arquivo, 'r') as arquivo:
            # Lê o conteúdo do arquivo
            conteudo = arquivo.read()
            # Imprime o conteúdo
            print(f'{conteudo}')
    except Exception as e:
        print(f'Ocorreu um erro: {e}')


# Exemplo de uso
mensagem_input = input('Digite a mensagem que deseja salvar no arquivo: ')
nome_do_arquivo = input('Digite o nome do arquivo (com extensão .txt): ')

escrever_em_arquivo(mensagem_input, nome_do_arquivo)

# Exemplo de uso
nome_do_arquivo = input('Digite o nome do arquivo a ser lido (com extensão .txt): ')

ler_e_imprimir_arquivo(nome_do_arquivo)
