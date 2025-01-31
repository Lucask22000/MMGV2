import streamlit as st
import os

# Desativa a navegação automática, removendo o menu de páginas
st.set_page_config(initial_sidebar_state="collapsed", page_title="Minha Página")

st.title("Home")

# Verifica se o usuário está logado
if "usuario" in st.session_state:
    usuario = st.session_state["usuario"]
    st.write(f"Bem-vindo, {usuario['nome']} {usuario['sobrenome']}! 📌")
    st.write(f"Seu telefone: {usuario['telefone']}")
else:
    st.warning("Você não está logado! Retorne à página de login.")