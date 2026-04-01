import streamlit as st
import pandas as pd
from supabase import create_client, Client

# -----------------------------
# CONFIG SUPABASE
# -----------------------------
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# -----------------------------
# FUNÇÕES CRUD
# -----------------------------

def create_jogador(nome, senha, apelido):
    supabase.table("jogador").insert({
        "nome_jogador": nome,
        "senha_jogador": senha,
        "apelido_jogador": apelido
    }).execute()


def read_jogadores():
    response = supabase.table("jogador").select("*").order("id_jogador").execute()
    return pd.DataFrame(response.data)


def update_jogador(id_jogador, nome, senha, apelido):
    supabase.table("jogador").update({
        "nome_jogador": nome,
        "senha_jogador": senha,
        "apelido_jogador": apelido
    }).eq("id_jogador", id_jogador).execute()


def delete_jogador(id_jogador):
    supabase.table("jogador").delete().eq("id_jogador", id_jogador).execute()

# -----------------------------
# UI STREAMLIT
# -----------------------------

st.set_page_config(page_title="CRUD Jogador", layout="wide")
st.title("🎮 CRUD de Jogadores (Supabase)")

menu = st.sidebar.selectbox("Menu", ["Visualizar", "Criar", "Atualizar", "Deletar"])

# -----------------------------
# VISUALIZAR
# -----------------------------
if menu == "Visualizar":
    st.subheader("Lista de Jogadores")
    df = read_jogadores()
    st.dataframe(df, use_container_width=True)

# -----------------------------
# CRIAR
# -----------------------------
elif menu == "Criar":
    st.subheader("Novo Jogador")

    nome = st.text_input("Nome")
    senha = st.text_input("Senha", type="password")
    apelido = st.text_input("Apelido")

    if st.button("Salvar"):
        if nome:
            create_jogador(nome, senha, apelido)
            st.success("Jogador criado com sucesso!")
        else:
            st.error("Nome é obrigatório")

# -----------------------------
# ATUALIZAR
# -----------------------------
elif menu == "Atualizar":
    st.subheader("Atualizar Jogador")

    df = read_jogadores()

    if not df.empty:
        selected_id = st.selectbox("Selecione o ID", df["id_jogador"])
        jogador = df[df["id_jogador"] == selected_id].iloc[0]

        nome = st.text_input("Nome", jogador["nome_jogador"])
        senha = st.text_input("Senha", jogador["senha_jogador"], type="password")
        apelido = st.text_input("Apelido", jogador["apelido_jogador"])

        if st.button("Atualizar"):
            update_jogador(selected_id, nome, senha, apelido)
            st.success("Atualizado com sucesso!")
    else:
        st.warning("Nenhum jogador encontrado")

# -----------------------------
# DELETAR
# -----------------------------
elif menu == "Deletar":
    st.subheader("Deletar Jogador")

    df = read_jogadores()

    if not df.empty:
        selected_id = st.selectbox("Selecione o ID para deletar", df["id_jogador"])

        if st.button("Deletar"):
            delete_jogador(selected_id)
            st.success("Deletado com sucesso!")
    else:
        st.warning("Nenhum jogador encontrado")
