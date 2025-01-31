import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date, datetime, timedelta
import time
from st_aggrid import AgGrid, GridOptionsBuilder
import sqlite3

# Ocultar a opção da página de login na sidebar
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] ul li a[href*="app"] {
            display: none !important;
        }
            [data-testid="stSidebarNav"] ul li a[href*="Cadastro"] {
            display: none !important;
        }
    </style>
""", unsafe_allow_html=True)

# Criando o Botão de Logout
def logout():
    st.session_state.clear()  # Limpa a sessão
    st.rerun()  # Atualiza a página

st.sidebar.button("❌ Encerrar Sessão", on_click=logout)

# Verifica se o usuário está logado
if "usuario" not in st.session_state:
    for i in range(10, 0, -1):
        st.warning(f"Encerrando sessão em {i} segundos... ⏳")
        time.sleep(1)
        st.switch_page("app.py")  # Redireciona para a tela de login

# Verifica se o usuário está logado
if "usuario" in st.session_state:
    usuario = st.session_state["usuario"]
    admin_badge = "👑 Sua conta é adiministradora do sistema!" if usuario.get("admin", False) else ""
    st.write(admin_badge)
    st.subheader(f"Bem-vindo, {usuario['nome']} {usuario['sobrenome']}!")
    
    is_admin = usuario.get("admin", False)  # Define se o usuário é admin
else:
    st.warning("Você não está logado! Retorne à página de login.")
    st.stop()  # Interrompe a execução do código se o usuário não estiver logado

# Configuração da página de agendamento
st.title("📅 Agendamento Diário")

# Função para carregar agendamentos do banco de dados
def carregar_agendamentos():
    conn = sqlite3.connect("banco.db")
    query = "SELECT * FROM nova_agenda"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Carregar os dados dos agendamentos
agendamentos = carregar_agendamentos()

# Configurar a tabela com colunas autoajustáveis
gb = GridOptionsBuilder.from_dataframe(agendamentos)
# Aplicar auto-ajuste de colunas
gb.configure_default_column(resizable=True, wrapText=True, autoHeight=True)
gb.configure_grid_options(domLayout='autoHeight', autoSizeColumns=True)
gb.configure_pagination(paginationAutoPageSize=True)  # Paginação automática
gb.configure_side_bar()  # Barra lateral com filtros
gb.configure_selection("multiple", use_checkbox=True)  # Seleção com checkbox

# Construir opções da grade
grid_options = gb.build()

# Exibir tabela interativa
grid_response = AgGrid(
    agendamentos,
    gridOptions=grid_options,
    height=500,
    fit_columns_on_grid_load=True,  # Agora as colunas ajustam automaticamente
    enable_enterprise_modules=True
)

# Exibir seleção de linhas
selecionados = grid_response["selected_rows"]
if selecionados:
    st.write("🔍 **Agendamentos Selecionados:**")
    st.dataframe(pd.DataFrame(selecionados))

# Para rodar: streamlit run seu_arquivo.py



