import os
from uuid import UUID

import httpx
import streamlit as st

from componentes import CardConteudo

API = os.getenv("FORUM_API_URL", "http://127.0.0.1:8000").rstrip("/")


def consultar(caminho):
    try:
        resposta = httpx.get(f"{API}{caminho}", timeout=5)
        resposta.raise_for_status()
    except httpx.HTTPStatusError as erro:
        if erro.response.status_code in (404, 422):
            st.warning("Pergunta não encontrada.")
        else:
            st.error(f"Falha ao consultar o fórum (HTTP {erro.response.status_code}).")
        st.stop()
    except httpx.RequestError:
        st.error("Não foi possível conectar à API do fórum.")
        st.stop()
    return resposta.json()


st.set_page_config(page_title="Fórum")
pergunta_id = st.query_params.get("pergunta")

if pergunta_id:
    if st.button("Voltar às perguntas"):
        del st.query_params["pergunta"]
        st.rerun()

    try:
        pergunta_id = UUID(pergunta_id)
    except ValueError:
        st.warning("Identificador de pergunta inválido.")
        st.stop()

    pergunta = consultar(f"/perguntas/{pergunta_id}")
    CardConteudo(pergunta, "pergunta", mostrar_tags=True, mostrar_status=True)
    st.header("Respostas")
    for resposta in pergunta["respostas"]:
        CardConteudo(resposta, "resposta", destaque_aceita=True)
    st.header("Comentários")
    for comentario in pergunta["comentarios"]:
        CardConteudo(comentario, "comentario")
else:
    st.title("Perguntas")
    perguntas = consultar("/perguntas")
    if not perguntas:
        st.info("Nenhuma pergunta publicada.")
    for pergunta in perguntas:
        CardConteudo(pergunta, "pergunta", mostrar_tags=True, mostrar_status=True)
        if st.button("Abrir pergunta", key=pergunta["id"]):
            st.query_params["pergunta"] = pergunta["id"]
            st.rerun()
