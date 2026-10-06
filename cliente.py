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

def menu():

    while True:
        print('\n=== CLIENTE API DE LIVROS ===')
        print('\n1 -Listar Livros')
        print('0 -Sair')

        opc = input('Escolha a opção desejada:').strip()


        if opc == '1':
            listar_livros()

        elif opc == '0':
            print('Encerrando programa...')
            break


if __name__ == '__main__':
    menu()