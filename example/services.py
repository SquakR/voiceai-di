"""
Модуль, содержащий сервисы для примера.
"""

from typing import Protocol, Self

from .repositories import ValuesRepositoryProtocol


class SumServiceProtocol(Protocol):
    """
    Протокол сервиса для сложения.
    """

    def sum(self: Self, *args: int) -> int:
        """
        Суммируем значения, полученные из аргумента, со значениями из репозитория.
        """
        ...


class SumServiceImpl:
    """
    Реализация сервиса для сложения.
    """

    def __init__(self, values_repository: ValuesRepositoryProtocol) -> None:
        self.values_repository = values_repository

    def sum(self: Self, *args: int) -> int:
        """
        Суммируем значения, полученные из аргумента, со значениями из репозитория.
        """
        return sum([*args, *self.values_repository.get_values()])
