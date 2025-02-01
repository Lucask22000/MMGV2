import streamlit as st
import pandas as pd
import calendar
from datetime import datetime
from Controller import carregar_agendamentos

# Função para criar o calendário
def criar_calendario(agendamentos_df, ano, mes):
    # Converte a coluna DATA para datetime
    agendamentos_df['DATA'] = pd.to_datetime(agendamentos_df['DATA'], format='%Y-%m-%d', errors='coerce')
    
    # Remove linhas com valores inválidos na coluna DATA
    agendamentos_df = agendamentos_df.dropna(subset=['DATA'])

    # Filtra os agendamentos para o mês e ano especificados
    agendamentos_mes = agendamentos_df[
        (agendamentos_df['DATA'].dt.year == ano) & 
        (agendamentos_df['DATA'].dt.month == mes)
    ]

    # Agrupa os agendamentos por data
    agendamentos_por_dia = agendamentos_mes.groupby(agendamentos_mes['DATA'].dt.day).size()
    nomes_por_dia = agendamentos_mes.groupby(agendamentos_mes['DATA'].dt.day)['NOME'].apply(list)

    # Encontra o mínimo e máximo de agendamentos para o gradiente
    min_agendamentos = agendamentos_por_dia.min() if not agendamentos_por_dia.empty else 0
    max_agendamentos = agendamentos_por_dia.max() if not agendamentos_por_dia.empty else 1

    # Cria o calendário
    cal = calendar.HTMLCalendar()
    html_cal = cal.formatmonth(ano, mes)

    # Data atual
    hoje = datetime.now().day if datetime.now().month == mes and datetime.now().year == ano else None

    # Adiciona os agendamentos ao calendário
    for dia, num_agendamentos in agendamentos_por_dia.items():
        # Calcula a cor do gradiente
        if max_agendamentos == min_agendamentos:
            cor = "#d4f7d4"  # Cor padrão se todos os dias tiverem o mesmo número de agendamentos
        else:
            intensidade = (num_agendamentos - min_agendamentos) / (max_agendamentos - min_agendamentos)
            cor = f"rgb({int(210 - intensidade * 150)}, {int(245 - intensidade * 150)}, {int(210 - intensidade * 150)})"

        # Adiciona a borda vermelha para a data atual
        borda = "2px solid red" if dia == hoje else "none"

        # Adiciona os nomes dos usuários agendados
        nomes = nomes_por_dia.get(dia, [])
        nomes_html = "<br>".join([f"<div style='background: #f0f0f0; margin: 2px; padding: 2px; border-radius: 3px;'>{nome}</div>" for nome in nomes])

        # Substitui a célula do dia no calendário
        html_cal = html_cal.replace(
            f'>{dia}<', 
            f' style="background-color: {cor}; border: {borda};"><b>{dia}</b><br>{nomes_html}<'
        )

    return html_cal

# Configuração da página
st.set_page_config(page_title="Calendário de Agendamentos", page_icon="📅", layout="centered")

# CSS personalizado para melhorar o visual
st.markdown("""
    <style>
        /* Ocultar a sidebar */
        [data-testid="stSidebarNav"] ul li a[href*="app"] {
            display: none !important;
        }
        [data-testid="stSidebarNav"] ul li a[href*="Cadastro"] {
            display: none !important;
        }
        
        /* Estilo do container do formulário */
        .login-container {
            background-color: #ffffff;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
            max-width: 500px;
            width: 90%;
            margin: auto;
        }

        /* Estilo do calendário */
        .calendar {
            width: 100%;
            border-collapse: collapse;
        }
        .calendar th, .calendar td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: center;
        }
        .calendar th {
            background-color: #f2f2f2;
        }
        .calendar td:hover {
            background-color: #f5f5f5;
        }
    </style>
""", unsafe_allow_html=True)

# Barra lateral para filtros e logout
with st.sidebar:
    # Foto do usuário
    st.image("img/user_photo.png", width=100, use_column_width=True)  # Substitua pelo caminho da foto do usuário
    
    # Filtros
    st.title("Filtros")
    filtro_nome = st.text_input("Filtrar por nome:")
    filtro_telefone = st.text_input("Filtrar por telefone:")
    filtro_data = st.date_input("Filtrar por data:", value=None)
    
    # Botão de logout
    st.markdown("---")
    if st.button("❌ Sair"):
        st.session_state.clear()
        st.rerun()

# Título da página
st.title("📅 Calendário de Agendamentos")

# Carregar os dados dos agendamentos
agendamentos_df = carregar_agendamentos()

# Selecionar o ano e o mês
ano = st.selectbox("Selecione o ano:", range(2023, 2030))
mes = st.selectbox("Selecione o mês:", range(1, 13), format_func=lambda x: calendar.month_name[x])

# Gerar o calendário
html_cal = criar_calendario(agendamentos_df, ano, mes)

# Exibir o calendário
st.markdown(html_cal, unsafe_allow_html=True)