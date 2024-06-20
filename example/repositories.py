"""
Модуль, содержащий репозитории для примера.
"""

from collections.abc import Sequence
from typing import Protocol, Self


class ValuesRepositoryProtocol(Protocol):
    """
    Протокол репозитория для получения значений.
    """

    def get_values(self: Self) -> Sequence[int]:
        """
        Получаем значения.
        """
        ...


class ValuesRepositoryImpl:
    """
    Реализация репозитория для получения значений.
    """

    def get_values(self: Self) -> Sequence[int]:
        """
        Получаем значения.
        """
        return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
