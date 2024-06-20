"""
Модуль, содержащий варианты использования для примера.
"""

from typing import Protocol, Self

from .services import SumServiceProtocol


class SumUseCaseProtocol(Protocol):
    """
    Протокол варианта использования для сложения.
    """

    async def __call__(self: Self, a: int) -> int:
        """
        Выполняем действие.
        """
        ...


class SumUseCaseImpl:
    """
    Реализация варианта использования для сложения.
    """

    def __init__(self, sum_service: SumServiceProtocol) -> None:
        self.sum_service = sum_service

    async def __call__(self: Self, a: int) -> int:
        """
        Выполняем действие.
        """
        return self.sum_service.sum(a)
