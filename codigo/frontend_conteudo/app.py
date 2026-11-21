import os
from pathlib import Path
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


st.set_page_config(page_title="Fórum", page_icon="💬")
st.html("<style>" + Path(__file__).with_name("forum.css").read_text() + "</style>")
st.html('''<nav class="forum-nav" aria-label="Navegação principal">
    <a href="?" target="_self"><span aria-hidden="true">&gt;_</span> Fórum</a>
    <a class="forum-nav-link" href="?" target="_self">Perguntas</a>
</nav>''')
pergunta_id = st.query_params.get("pergunta")

if pergunta_id:
    st.html('<a class="forum-back" href="?" target="_self">← Todas as perguntas</a>')

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
    st.html('''<section class="forum-hero">
        <h1>Fórum de<br><em>perguntas.</em></h1>
        <div class="forum-art" aria-hidden="true"><i></i><b>&lt;/&gt;</b></div>
    </section>''')
    perguntas = consultar("/perguntas")
    busca = st.text_input("Buscar perguntas", placeholder="Buscar por título, assunto ou tag…")
    termo = busca.strip().casefold()
    perguntas = [p for p in perguntas if termo in " ".join(
        [p["titulo"], p["corpo"], *p["tags"]]
    ).casefold()]
    st.header("Resultados" if termo else "Discussões recentes")
    if not perguntas:
        st.info("Nenhuma pergunta encontrada." if termo else "Nenhuma pergunta publicada.")
    for pergunta in sorted(perguntas, key=lambda p: p["data_criacao"], reverse=True):
        CardConteudo(pergunta, "pergunta", mostrar_tags=True, mostrar_status=True, link_detalhe=True)
