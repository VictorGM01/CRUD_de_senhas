import sqlite3


conexao = sqlite3.connect("Senhas.bd")
c = conexao.cursor()

# Cria tabela para armazenar o nome do programa e a senha
c.execute('CREATE TABLE IF NOT EXISTS dados (programa text primary key, senha text)')

# salva
conexao.commit()


# função para criar/inserir nova senha
def insere_valores(programa: str, senha: str):
    c.execute(f'INSERT INTO dados VALUES ("{programa}", "{senha}")')
    conexao.commit()
