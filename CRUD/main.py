import sqlite3
import base64

from CRUD.excecoes import DelecaoInvalida


conexao = sqlite3.connect("Senhas.bd")
c = conexao.cursor()

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
        senha_bytes = senha.encode('utf-8')
        senha_64 = base64.b64encode(senha_bytes)
        c.execute(f'INSERT INTO usuario VALUES ("{nome}", "{senha_64}")')
        conexao.commit()
    except sqlite3.Error as erro_sql:
        print(f'Não foi possível criar o usuário. Erro: {erro_sql}')


# função para mudança de senha do usuário
def atualiza_senha_usuario(nome: str, nova_senha: str):
    try:
        senha_bytes = nova_senha.encode('utf-8')
        senha_64 = base64.b64encode(senha_bytes)
        c.execute(f'UPDATE usuario SET senha_user = "{senha_64}" WHERE nome_user = "{nome}"')
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
        senha_para_bytes = senha.encode(encoding='utf-8')
        senha_para_b64 = base64.b64encode(senha_para_bytes)
        c.execute(f'INSERT INTO dados VALUES ("{usuario}", "{programa}", "{senha_para_b64}")')
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
