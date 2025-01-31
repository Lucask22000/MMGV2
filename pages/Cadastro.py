import streamlit as st
from Controller import cadastrar_usuario

st.title("Cadastro de Usuário")

# Oculta completamente a barra lateral e o botão de expandir
st.markdown("""
    <style>
        [data-testid="stSidebar"], [data-testid="collapsedControl"] {
            display: none !important;
        }
    </style>
""", unsafe_allow_html=True)

# Entrada de dados
nome = st.text_input("Nome")
sobrenome = st.text_input("Sobrenome")
# Função para formatar telefone
def formatar_telefone(numero):
    numero = ''.join(filter(str.isdigit, numero))  # Remove caracteres não numéricos
    if len(numero) == 11:
        return f"({numero[:2]}) {numero[2:7]}-{numero[7:]}"
    elif len(numero) == 10:
        return f"({numero[:2]}) {numero[2:6]}-{numero[6:]}"
    return numero  # Retorna como está se não atender os critérios

# Campo de telefone
telefone = st.text_input("Informe um número válido com DDD", placeholder="(99) 99999-9999")
telefone_formatado = formatar_telefone(telefone)

if telefone.strip():
    st.write(f"📞 Você digitou: {telefone_formatado}")
senha = st.text_input("Senha", type="password")
confirmar_senha = st.text_input("Confirmar Senha", type="password")

if st.button("Cadastrar"):
    # Verificando se algum campo está vazio
    if not nome or not sobrenome or not telefone or not senha or not confirmar_senha:
        st.error("Todos os campos são obrigatórios!")
    elif senha != confirmar_senha:
        st.error("As senhas não coincidem!")
    else:
        if cadastrar_usuario(nome, sobrenome, telefone, senha):
            st.session_state["mensagem_sucesso"] = "Cadastro realizado com sucesso!"
            st.switch_page("app.py")  # Redireciona para a página inicial
        else:
            st.error("Erro: Telefone já cadastrado!")            