import streamlit as st
import time

# Criando o Botão de Logout
def logout(session_state):
    st.session_state.clear()  # Limpa a sessão
    for i in range(10, 0, -1):
        st.warning(f"Encerrando sessão em {i} segundos... ⏳")
        time.sleep(1)