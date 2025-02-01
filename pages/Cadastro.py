import streamlit as st
import pandas as pd
from Controller import cadastrar_usuario

st.title("Cadastro de Usuário")

# Ocultar a opção da página de login na sidebar
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] ul li a[href*="Painel"] {
            display: none !important;
        }
    </style>
""", unsafe_allow_html=True)

# Entrada de dados
nome = st.text_input("Nome")
sobrenome = st.text_input("Sobrenome")

# Função para formatar e validar telefone
def formatar_telefone(numero):
    numero = ''.join(filter(str.isdigit, numero))  # Remove caracteres não numéricos
    if len(numero) == 11:
        return f"({numero[:2]}) {numero[2:7]}-{numero[7:]}"
    elif len(numero) == 10:
        return f"({numero[:2]}) {numero[2:6]}-{numero[6:]}"
    return None  # Retorna None se não atender os critérios

# Campo de telefone
telefone = st.text_input("Informe um número válido com DDD", placeholder="(99) 99999-9999")
telefone_formatado = formatar_telefone(telefone)

if telefone.strip() and telefone_formatado:
    st.write(f"📞 Você digitou: {telefone_formatado}")
elif telefone.strip():
    st.error("Número de telefone inválido! Use o formato (99) 99999-9999 ou (99) 9999-9999.")

senha = st.text_input("Senha", type="password")
confirmar_senha = st.text_input("Confirmar Senha", type="password")

# Spin button para ativar o campo de administrador
ativar_admin = st.checkbox("Deseja adicionar um administrador?")

admin = False
chave_adm_incorreta = False
if ativar_admin:
    chave_adm = st.text_input("Chave de Administrador", type="password")
    if chave_adm == "adm123":
        admin = st.checkbox("Adicionar como Administrador")
    elif chave_adm:
        chave_adm_incorreta = True

# Mensagem de erro para chave de administrador incorreta
if chave_adm_incorreta:
    st.error("Chave de administrador incorreta!")

if st.button("Cadastrar"):
    # Verificando se algum campo está vazio
    if not nome or not sobrenome or not telefone or not senha or not confirmar_senha:
        st.error("Todos os campos são obrigatórios!")
    elif senha != confirmar_senha:
        st.error("As senhas não coincidem!")
    else:
        if telefone_formatado and cadastrar_usuario(nome, sobrenome, telefone_formatado, senha, admin):
            st.session_state["mensagem_sucesso"] = "Cadastro realizado com sucesso!"
            st.experimental_rerun()  # Redireciona para a página inicial
        else:
            st.error("Erro: Telefone já cadastrado ou inválido!")

