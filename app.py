import streamlit as st
from Controller import verificar_login

# Ocultar a opção da página de login na sidebar
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] ul li a[href*="app"] {
            display: none !important;
        }
            [data-testid="stSidebarNav"] ul li a[href*="Painel"] {
            display: none !important;
        }
    </style>
""", unsafe_allow_html=True)

# Título e imagem
st.markdown("<h1 style='text-align: center; color: DarkGray;'>Bem-vindo(a) à agenda MMG</h1>", unsafe_allow_html=True)
st.image("img/imglogin.png", width=700)

# Verifica se há uma mensagem de sucesso armazenada
if "mensagem_sucesso" in st.session_state:
    st.success(st.session_state["mensagem_sucesso"])
    del st.session_state["mensagem_sucesso"]  # Remove a mensagem após exibição

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

# Campo de senha
senha = st.text_input("Digite sua senha", type="password", placeholder="********", key="senha_login")

# Botão de login
if st.button("Entrar"):
    usuario = verificar_login(telefone_formatado, senha)
    if usuario:  # Se encontrou um usuário no banco
        # Salvando os dados do usuário na sessão
        st.session_state["usuario"] = {
            "id": usuario[0],
            "nome": usuario[1],
            "sobrenome": usuario[2],
            "telefone": usuario[3],
            "admin": usuario[4]
        }
        st.switch_page("pages/Painel.py")  # Redireciona para a Painel
    else:
        st.error("Número de telefone ou senha inválidos.")

# Botão para ir para a página de cadastro
if st.button("Não tem uma conta? Cadastre-se aqui!"):
    st.switch_page("pages/Cadastro.py")