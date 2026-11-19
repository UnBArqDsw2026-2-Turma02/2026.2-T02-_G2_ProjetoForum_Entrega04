from typing import Literal

import streamlit as st


def ListaTags(tags: list[str]) -> None:
    if tags:
        st.text("Tags · " + ", ".join(tags))


def CardConteudo(
    item: dict,
    variante: Literal["pergunta", "resposta", "comentario"],
    *,
    mostrar_tags: bool = False,
    mostrar_status: bool = False,
    destaque_aceita: bool = False,
) -> None:
    with st.container(border=True):
        if variante == "pergunta":
            st.subheader(item["titulo"])
        if mostrar_status:
            st.caption(item["status"])
        if destaque_aceita and item.get("aceita"):
            st.success("Resposta aceita")
        st.text(item["corpo"])
        st.text(f'{item["autor"]} · {item["data_criacao"]}')
        if mostrar_tags:
            ListaTags(item["tags"])
