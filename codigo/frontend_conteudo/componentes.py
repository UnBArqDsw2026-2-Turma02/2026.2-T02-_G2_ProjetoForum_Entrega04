from datetime import datetime
from html import escape
from typing import Literal
from uuid import UUID

import streamlit as st


def ListaTags(tags: list[str]) -> str:
    return "".join(f'<span class="forum-tag">{escape(tag)}</span>' for tag in tags)


def quantidade(total: int, singular: str, plural: str) -> str:
    return f"{total} {singular if total == 1 else plural}"


def CardConteudo(
    item: dict,
    variante: Literal["pergunta", "resposta", "comentario"],
    *,
    mostrar_tags: bool = False,
    mostrar_status: bool = False,
    destaque_aceita: bool = False,
    link_detalhe: bool = False,
) -> None:
    autor = escape(item["autor"])
    data = datetime.fromisoformat(item["data_criacao"]).strftime("%d/%m/%Y às %H:%M")
    titulo = ""
    rodape = ""
    if variante == "pergunta":
        texto = escape(item["titulo"])
        if link_detalhe:
            url = f'?pergunta={UUID(item["id"])}'
            texto = f'<a href="{url}" target="_self">{texto} <span aria-hidden="true">↗</span></a>'
            respostas = quantidade(len(item["respostas"]), "resposta", "respostas")
            comentarios = quantidade(len(item["comentarios"]), "comentário", "comentários")
            rodape = f'<footer>{respostas} · {comentarios}</footer>'
        titulo = f"<h2>{texto}</h2>"
    status = escape(item["status"].capitalize()) if mostrar_status else ""
    if destaque_aceita and item.get("aceita"):
        status = "Resposta aceita"
    selo = f'<span class="forum-status">{status}</span>' if status else ""
    tags = ListaTags(item["tags"]) if mostrar_tags else ""
    st.html(f"""
        <article class="forum-card forum-{variante}">
            <div class="forum-meta">
                <span class="forum-avatar" aria-hidden="true">{escape(item['autor'][:1].upper())}</span>
                <strong>{autor}</strong><time>{data}</time>{selo}
            </div>
            {titulo}<p class="forum-body">{escape(item['corpo'])}</p>
            {tags}{rodape}
        </article>
    """)
