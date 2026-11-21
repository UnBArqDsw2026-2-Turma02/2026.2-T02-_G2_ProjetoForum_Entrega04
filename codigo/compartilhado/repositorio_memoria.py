from threading import RLock
from typing import Generic, Protocol, TypeVar

K = TypeVar("K")
V = TypeVar("V")


class RepositorioBase(Protocol[K, V]):
    """Contrato de persistência por chave. Atualizar e remover exigem chave existente."""

    def salvar(self, chave: K, valor: V) -> None: ...
    def buscar_por_id(self, chave: K) -> V | None: ...
    def atualizar(self, chave: K, valor: V) -> None: ...
    def listar(self) -> list[V]: ...
    def remover(self, chave: K) -> None: ...
    def limpar(self) -> None: ...


class RepositorioEmMemoria(Generic[K, V]):
    """Armazena referências e protege cada operação com um lock reentrante."""

    def __init__(self) -> None:
        self._dados: dict[K, V] = {}
        self._lock = RLock()

    def salvar(self, chave: K, valor: V) -> None:
        with self._lock:
            self._dados[chave] = valor

    def buscar_por_id(self, chave: K) -> V | None:
        with self._lock:
            return self._dados.get(chave)

    def atualizar(self, chave: K, valor: V) -> None:
        with self._lock:
            if chave not in self._dados:
                raise KeyError(chave)
            self._dados[chave] = valor

    def listar(self) -> list[V]:
        with self._lock:
            return list(self._dados.values())

    def remover(self, chave: K) -> None:
        with self._lock:
            del self._dados[chave]

    def limpar(self) -> None:
        with self._lock:
            self._dados.clear()
