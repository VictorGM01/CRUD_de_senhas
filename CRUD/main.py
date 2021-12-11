import sqlite3
from cryptography.fernet import Fernet
import PySimpleGUI as sg

from CRUD.excecoes import DelecaoInvalida


conexao = sqlite3.connect("Senhas.bd")
c = conexao.cursor()


def criptografa_file():
    with open(
            r'C:\Users\victo\PycharmProjects\cybersecurity\criptografia\criptografar_arquivo\chave_simetrica.txt', 'rb'
    ) as f:
        cr = f.read()

    f = Fernet(cr)

    with open('Senhas.bd', 'rb') as arquivo:
        arquivo_original = arquivo.read()

    with open('Senhas.bd', 'wb') as cript:
        cript.write(f.encrypt(arquivo_original))


def descriptografa_file():
    with open(
            r'C:\Users\victo\PycharmProjects\cybersecurity\criptografia\criptografar_arquivo\chave_simetrica.txt', 'rb'
    ) as f:
        cr = f.read()

    f = Fernet(cr)

    with open('Senhas.bd', 'rb') as arquivo:
        criptografado = arquivo.read()

    with open('Senhas.bd', 'wb') as cript:
        cript.write(f.decrypt(criptografado))


# Cria tabela para armazenar informações do usuário
try:
    c.execute('CREATE TABLE IF NOT EXISTS usuario (nome_user text PRIMARY KEY, senha_user text)')
    conexao.commit()
except sqlite3.Error:
    print(f'Erro: {sqlite3.Error}')

# Cria tabela para armazenar o nome do programa e a senha
try:
    c.execute('''CREATE TABLE IF NOT EXISTS dados (nome_usuario text, programa text primary key, senha text,
    CONSTRAINT fk_usuario FOREIGN KEY(nome_usuario) REFERENCES usuario(nome_user))''')
    conexao.commit()
except sqlite3.Error:
    print(f'Erro: {sqlite3.Error}')


# função para criar novo usuário (útil para a GUI)
def cria_usuario(nome: str, senha: str):
    try:
        c.execute(f'INSERT INTO usuario VALUES ("{nome}", "{senha}")')
        conexao.commit()
    except sqlite3.Error as erro_sql:
        print(f'Não foi possível criar o usuário. Erro: {erro_sql}')


# função para mudança de senha do usuário
def atualiza_senha_usuario(nome: str, nova_senha: str):
    try:
        c.execute(f'UPDATE usuario SET senha_user = "{nova_senha}" WHERE nome_user = "{nome}"')
        conexao.commit()
    except sqlite3.Error:
        print(f'Erro: {sqlite3.Error}')


# função para criar/inserir nova senha
def insere_valores(usuario: str, programa: str, senha: str):
    c.execute('SELECT programa FROM dados')
    programas = c.fetchall()

    lista_de_programas = []
    for i in programas:
        lista_de_programas.append(i[0])

    if programa not in lista_de_programas:
        c.execute(f'INSERT INTO dados VALUES ("{usuario}", "{programa}", "{senha}")')
        conexao.commit()

    else:
        print(f'A senha para "{programa}" já está cadastrada!')


# função para excluir uma senha armazenada por meio do nome do programa
def exclui_valores(programa: str):
    c.execute('SELECT programa FROM dados')
    resultado = c.fetchall()

    resultados = []
    for res in resultado:
        resultados.append(res[0])

    if programa in resultados:
        c.execute(f'DELETE FROM dados WHERE programa = "{programa}"')
        conexao.commit()

    else:
        raise DelecaoInvalida('Não foi possível concluir a deleção')


# função para atualizar a senha por meio do nome do programa
def atualiza_valores(programa: str, nova_senha: str):
    try:
        c.execute(f'UPDATE dados SET senha = "{nova_senha}" WHERE programa = "{programa}"')
        conexao.commit()
    except sqlite3.Error:
        print(f'Erro: {sqlite3.Error}')


# função que possibilita a viisualização da senha do programa informado
def leitura_de_valores_especificos(programa: str):
    try:
        c.execute(f'SELECT senha FROM dados WHERE programa = "{programa}"')
        resultado = c.fetchall()
        print(resultado[0][0])

    except sqlite3.Error:
        print(f'Erro: {sqlite3.Error}')


# função que retorna todos os dados armazenados no banco de dados
def leitura_de_todas_as_senhas():
    try:
        c.execute('SELECT * FROM dados')
        resultado = c.fetchall()

        for dados in resultado:
            print(f'Programa: {dados[1]} - Senha: {dados[2]}')

    except sqlite3.Error:
        print(f'Erro: {sqlite3.Error}')
