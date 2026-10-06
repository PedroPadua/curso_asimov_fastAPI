import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

api_url = os.getenv('api_url')

def trat_resp(resp: requests.Response):
    """Imprime a resposta API, lidando com erros"""

    try:
        data = resp.json()

    except ValueError:
        print(f'\nStatus: {resp.status_code}')
        print('Resposta sem JSON')
        print(resp.text)
        return

    if resp.status_code >= 400:
        print(f'\nErro: {resp.status_code}')
    else:
        print(json.dumps(data, indent =4, ensure_ascii=False))


def listar_livros():
    resp = requests.get(f'{api_url}/livros')
    print('\nListar Livros:')
    trat_resp(resp)

def obter_livro():
    livro_id = input('UUID do livro:').strip()
    resp = requests.get(f'{api_url}/livros/{livro_id}')
    print('Livro pelo UUID:')
    trat_resp(resp)


def add_livro():
    print('\nDigite os dados do novo livro:')
    autor = input('Autor:')
    titulo = input('Título:')
    editora = input('Editora:')
    ano = input('Ano:')

    payload = {
        'autor' : autor,
        'titulo': titulo, 
        'editora': editora,
        'ano': ano
    }
    resp = requests.post(f'{api_url}/livros/', json = payload)
    print('Livro adicionado!')

def edite_livro():
    livro_id = input('UUID do livro:').strip()
    print('\nDigite os dados do livro a ser editado:')
    autor = input('Autor:')
    titulo = input('Título:')
    editora = input('Editora:')
    ano = input('Ano:')

    payload = {
        'uuid': livro_id,
        'autor' : autor,
        'titulo': titulo, 
        'editora': editora,
        'ano': ano        
    }

    resp = requests.put(f'{api_url}/livros/{livro_id}', json = payload)
    print('\nLivro atualizado!')


def menu():

    while True:
        print('\n=== CLIENTE API DE LIVROS ===')
        print('\n1 -Listar Livros')
        print('2 -Buscar livro por UUID')
        print('3 -Adicionar novo livro')
        print('4 -Editar livro existente')
        print('0 -Sair')

        opc = input('Escolha a opção desejada:').strip()


        if opc == '1':
            listar_livros()

        elif opc == '2':
            obter_livro()

        elif opc == '3':
            add_livro()
        
        elif opc == '4':
            edite_livro()

        elif opc == '0':
            print('Encerrando programa...')
            break

        else:
            print('Opção Inválida!')


if __name__ == '__main__':
    menu()