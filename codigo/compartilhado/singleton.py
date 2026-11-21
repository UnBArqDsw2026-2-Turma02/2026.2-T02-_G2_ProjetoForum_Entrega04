from threading import Lock
from typing import Self


class Singleton:
    """Uma instância por subclasse concreta e por processo."""

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._instancia = None
        cls._token = object()
        cls._lock = Lock()

    def __init__(self, token=None):
        if token is not type(self)._token:
            raise TypeError(f"Use {type(self).__name__}.instancia()")

    @classmethod
    def instancia(cls) -> Self:
        instancia = cls._instancia
        if instancia is None:
            with cls._lock:
                instancia = cls._instancia
                if instancia is None:
                    instancia = cls(cls._token)
                    cls._instancia = instancia
        return instancia

    @classmethod
    def _resetar(cls) -> None:
        """Descarta a instância da subclasse para isolamento entre testes."""
        with cls._lock:
            cls._instancia = None
