"""
Модуль, содержащий контейнер для примера.
"""

from typing import Annotated

from va_di.container import BaseContainer

from .repositories import ValuesRepositoryImpl, ValuesRepositoryProtocol
from .services import SumServiceImpl, SumServiceProtocol
from .use_cases import SumUseCaseImpl, SumUseCaseProtocol


class Container(BaseContainer):
    """
    IoC контейнер для примера.
    """

    values_repository: Annotated[ValuesRepositoryProtocol, ValuesRepositoryImpl]
    sum_service: Annotated[SumServiceProtocol, SumServiceImpl]
    sum_use_case: Annotated[SumUseCaseProtocol, SumUseCaseImpl]
