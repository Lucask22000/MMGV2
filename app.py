import streamlit as st
from Controller import verificar_login

# Configuração da página
st.set_page_config(
    page_title="Login - MMG Montagens",
    page_icon="🛠️",
    layout="centered",
    initial_sidebar_state="collapsed"  # Colapsa a barra lateral
)

# CSS personalizado para melhorar o visual
st.markdown("""
    <style>
        /* Centraliza o conteúdo */
        .stApp {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        
        /* Estilo do container do formulário */
        .login-container {
            background-color: #ffffff;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
            max-width: 400px;
            width: 100%;
            margin: auto;
        }
        
        /* Estilo dos campos de entrada */
        .stTextInput input, .stTextInput input:focus {
            border: 1px solid #cccccc;
            border-radius: 5px;
            padding: 10px;
            width: 100%;
        }
        
        /* Estilo dos botões */
        .stButton button {
            background-color: #2c3e50;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            width: 100%;
            font-size: 16px;
            cursor: pointer;
        }
        
        .stButton button:hover {
            background-color: #34495e;
        }
        
        /* Estilo do link de cadastro */
        .stButton a {
            color: #2c3e50;
            text-decoration: none;
            font-weight: bold;
        }
        
        .stButton a:hover {
            text-decoration: underline;
        }
        
        /* Ocultar a sidebar */
        [data-testid="stSidebarNav"] {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)

# Container do formulário de login
with st.container():
    # CSS personalizado para melhorar o visual
    st.markdown("""
    <style>
        /* Estilo do container do formulário */
        .login-container {
            background-color: blue;
            padding: 3rem;  /* Aumentei o padding para dar mais espaço interno */
            border-radius: 10px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
            max-width: 500px;  /* Aumentei a largura máxima */
            width: 90%;  /* Aumentei a largura relativa */
            margin: auto;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Carregar a imagem do logo
    try:
        st.image("img/imglogin.png", width=200, use_container_width=True)  # Substitua pelo caminho da sua logo
    except FileNotFoundError:
        st.error("Erro: Arquivo de logo não encontrado. Verifique o caminho da imagem.")
    
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
    telefone = st.text_input("📱 Telefone", placeholder="(99) 99999-9999")
    telefone_formatado = formatar_telefone(telefone)

    # Campo de senha
    senha = st.text_input("🔒 Senha", type="password", placeholder="********", key="senha_login")

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
            st.success("Login realizado com sucesso! Redirecionando...")
            st.switch_page("pages/Painel.py")  # Redireciona para a Painel
        else:
            st.error("Número de telefone ou senha inválidos.")

    # Botão para ir para a página de cadastro
    st.markdown("<div style='text-align: center; margin-top: 1rem;'>", unsafe_allow_html=True)
    if st.button("Não tem uma conta? Cadastre-se aqui!"):
        st.switch_page("pages/Cadastro.py")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)