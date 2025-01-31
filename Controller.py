import sqlite3
import streamlit as st

def conectar_bd():
    conn = sqlite3.connect("banco.db")  # Cria ou conecta ao banco de dados
    cursor = conn.cursor()
    
    # Criar a tabela de usuários (se não existir)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            sobrenome TEXT NOT NULL,
            telefone TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

# Chame essa função ao iniciar a aplicação para garantir que o banco de dados exista
conectar_bd()

def cadastrar_usuario(nome, sobrenome, telefone, senha):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    
    try:
        cursor.execute("INSERT INTO usuarios (nome, sobrenome, telefone, senha) VALUES (?, ?, ?, ?)", 
            (nome, sobrenome, telefone, senha))
        conn.commit()
        return True  # Sucesso
    except sqlite3.IntegrityError:
        return False  # Erro: telefone já cadastrado
    finally:
     conn.close()  

def verificar_login(telefone, senha):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE telefone = ? AND senha = ?", (telefone, senha))
    usuario = cursor.fetchone()  # Retorna None se não encontrar

    conn.close()
    return usuario  # Retorna os dados do usuário se encontrar
