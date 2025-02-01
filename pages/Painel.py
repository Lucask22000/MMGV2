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
            cor = "#e3f2fd"  # Cor padrão se todos os dias tiverem o mesmo número de agendamentos
        else:
            intensidade = (num_agendamentos - min_agendamentos) / (max_agendamentos - min_agendamentos)
            cor = f"rgba(33, 150, 243, {intensidade * 0.7 + 0.3})"  # Gradiente azul

        # Adiciona a borda para a data atual
        borda = "2px solid #ff5252" if dia == hoje else "none"

        # Adiciona os nomes dos usuários agendados
        nomes = nomes_por_dia.get(dia, [])
        nomes_html = "<br>".join([f"<div style='background: #ffffff; margin: 2px; padding: 2px; border-radius: 3px; color: #333; font-size: 12px;'>{nome}</div>" for nome in nomes])

        # Substitui a célula do dia no calendário
        html_cal = html_cal.replace(
            f'>{dia}<', 
            f' style="background-color: {cor}; border: {borda}; border-radius: 8px; padding: 10px; color: #333; font-weight: bold;"><b>{dia}</b><br>{nomes_html}<'
        )

    return html_cal

# Configuração da página
st.set_page_config(page_title="Calendário de Agendamentos", page_icon="📅", layout="centered")

# CSS personalizado para um visual moderno
st.markdown("""
    <style>
        /* Estilo geral */
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f5f5f5;
        }

        .calendar {
        width: 100%; /* Ocupa a mesma largura dos inputs */
        border-collapse: separate;
        border-spacing: 8px;
    }

    /* Aumentar a espessura das bordas */
    .calendar th, .calendar td {
        border: 2px solid #ddd; /* Bordas mais grossas */
        padding: 12px;
        text-align: center;
        border-radius: 8px;
    }

    /* Estilo para o cabeçalho do calendário */
    .calendar th {
        background-color: #2196f3;
        color: white;
        font-size: 14px;
        border: 2px solid #2196f3; /* Bordas mais grossas */
    }

    /* Efeito de hover nas células */
    .calendar td:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }

        /* Estilo para a imagem redonda */
        .profile-img {
            border-radius: 50%;
            width: 100px;
            height: 100px;
            object-fit: cover;
            margin-bottom: 16px;
            border: 2px solid #2196f3;
        }

        /* Estilo da barra lateral */
        .sidebar .sidebar-content {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        /* Estilo dos botões */
        .stButton button {
            background-color: #2196f3;
            color: white;
            border-radius: 8px;
            padding: 10px 20px;
            font-size: 14px;
            border: none;
            transition: background-color 0.2s;
        }
        .stButton button:hover {
            background-color: #1976d2;
        }

        /* Estilo dos inputs */
        .stTextInput input, .stDateInput input {
            border-radius: 8px;
            border: 1px solid #ddd;
            padding: 10px;
            font-size: 14px;
        }
    </style>
""", unsafe_allow_html=True)

# Barra lateral para filtros e logout
with st.sidebar:
    # Foto do usuário

    st.image("img/user_photo.png", width=100, use_container_width=True)

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