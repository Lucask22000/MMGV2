import sqlite3
import pandas as pd

# Criar a tabela de usuários (se não existir)
def conectar_bd():
    conn = sqlite3.connect("banco.db")  # Cria ou conecta ao banco de dados
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            sobrenome TEXT NOT NULL,
            telefone TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    ''')
    # Adicionar a coluna admin se não existir
    cursor.execute("PRAGMA table_info(usuarios);")
    columns = [column[1] for column in cursor.fetchall()]
    if 'admin' not in columns:
        cursor.execute("ALTER TABLE usuarios ADD COLUMN admin INTEGER NOT NULL DEFAULT 0;")
        conn.commit()
    conn.close()

# Chame essa função ao iniciar a aplicação para garantir que o banco de dados exista
conectar_bd()
def cadastrar_usuario(nome, sobrenome, telefone, senha, admin):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO usuarios (nome, sobrenome, telefone, senha, admin) VALUES (?, ?, ?, ?, ?)", 
        (nome, sobrenome, telefone, senha, int(admin)))
        conn.commit()
        return True  # Sucesso
    except sqlite3.IntegrityError:
        return False  # Erro: telefone já cadastrado
    finally:
        conn.close()  

# Verifica se esta logado
def verificar_login(telefone, senha):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE telefone = ? AND senha = ?", (telefone, senha))
    usuario = cursor.fetchone()  # Retorna None se não encontrar
    conn.close()
    return usuario  # Retorna os dados do usuário se encontrar

# Função para carregar agendamentos do banco de dados
def carregar_agendamentos(ID, DATA ,DATA_DO_AGENDAMENTO ,NOME ,TELEFONE):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute( "SELECT * FROM nova_agenda = ?", (ID, DATA ,DATA_DO_AGENDAMENTO ,NOME ,TELEFONE))
    agendamentos_df = cursor.fetchone()
    conn.close()
    return agendamentos_df

def carregar_agendamentos():
    # Conecta ao banco de dados
    conn = sqlite3.connect('banco.db')  # Substitua pelo nome do seu banco de dados
    cursor = conn.cursor()

    # Executa a consulta SQL para buscar os agendamentos
    query = "SELECT * FROM nova_agenda"
    cursor.execute(query)

    # Recupera os dados e converte em um DataFrame do Pandas
    dados = cursor.fetchall()
    colunas = [descricao[0] for descricao in cursor.description]
    agendamentos_df = pd.DataFrame(dados, columns=colunas)

    # Fecha a conexão com o banco de dados
    conn.close()

    return agendamentos_df
