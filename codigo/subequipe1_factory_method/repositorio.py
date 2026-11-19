from uuid import UUID

from compartilhado.repositorio_memoria import RepositorioBase, RepositorioEmMemoria
from compartilhado.singleton import Singleton

from .produtos import Conteudo, Pergunta


class RepositorioConteudo(Singleton):
    def __init__(self, token=None):
        super().__init__(token)
        self._memoria = RepositorioEmMemoria[UUID, Conteudo]()
        self._repositorio: RepositorioBase[UUID, Conteudo] = self._memoria

    @property
    def _conteudos(self) -> dict[UUID, Conteudo]:
        """Acesso legado ao dicionário da Entrega 03."""
        return self._memoria._dados

    def salvar(self, conteudo: Conteudo) -> None:
        self._repositorio.salvar(conteudo.id, conteudo)

    def buscar_por_id(self, conteudo_id: UUID) -> Conteudo | None:
        return self._repositorio.buscar_por_id(conteudo_id)

    def atualizar(self, conteudo: Conteudo) -> None:
        try:
            self._repositorio.atualizar(conteudo.id, conteudo)
        except KeyError:
            raise KeyError(f"Conteúdo {conteudo.id} não está no repositório") from None

    def listar_perguntas(self) -> list[Pergunta]:
        perguntas = []
        for conteudo in self._repositorio.listar():
            pergunta = conteudo.como_pergunta()
            if pergunta is not None:
                perguntas.append(pergunta)
        return perguntas
