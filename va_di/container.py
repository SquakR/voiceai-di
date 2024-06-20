"""
Модуль, содержащий базовый IoC контейнер.
"""

from __future__ import annotations

from collections.abc import Callable
from functools import partial
from typing import (
    Annotated,
    Any,
    Protocol,
    cast,
    get_args,
    get_origin,
    get_type_hints,
)

from fastapi import Request

from .exceptions import InvalidContainerError


class BaseContainerMeta(type):
    """
    Метакласс для построения IoC контейнера.
    """

    def __new__(cls, name: str, bases: tuple[type], classdict: dict[str, Any]) -> type:
        parents = [b for b in bases if isinstance(b, BaseContainerMeta)]
        if not parents:
            return super().__new__(cls, name, bases, classdict)
        props_mapping: dict[str, type] = {}
        types_mapping: dict[type, type] = {}
        new_classdict: dict[str, Any] = {
            '__props_mapping__': props_mapping,
            '__types_mapping__': types_mapping,
        }
        for k, v in classdict['__annotations__'].items():
            if get_origin(v) is not Annotated:
                raise InvalidContainerError(
                    f'Неправильный тип аннотации {k}: ожидалось typing.Annotated, получено {v}'
                )
            args = get_args(v)
            if len(args) != 2:
                raise InvalidContainerError(
                    f'Неверное число аргументов аннотации {k}: ожидалось 2, получено: {len(args)}'
                )
            protocol, impl = args
            if not issubclass(protocol, cast(type, Protocol)) or not isinstance(
                impl, type
            ):
                raise InvalidContainerError(f'Неверные аргументы аннотации {k}')
            props_mapping[k] = protocol
            types_mapping[protocol] = impl
        new_classdict['__init__'] = cls._make_init()
        new_classdict['__getattribute__'] = cls._make_get_getattribute()
        created_cls = super().__new__(cls, name, bases, new_classdict)
        for k in props_mapping.keys():
            cls.create_class_attr(created_cls, k)
        return created_cls

    @staticmethod
    def _make_init() -> Callable[[Any], None]:
        """
        Создаем метод __init__.
        """

        def __init__(self: Any) -> None:
            self.__created_impl__ = {}

        return __init__

    @classmethod
    def _make_get_getattribute(cls) -> Callable[[Any, str], None]:
        """
        Создаем метод __getattribute__.
        """

        def __getattribute__(self: Any, name: str) -> Any:
            props_mapping = object.__getattribute__(self, '__props_mapping__')
            types_mapping = object.__getattribute__(self, '__types_mapping__')
            created_impl = object.__getattribute__(self, '__created_impl__')
            protocol = props_mapping[name]
            impl = types_mapping[protocol]
            if created_impl.get(protocol) is None:
                created_impl[protocol] = cls._create_value(
                    impl, created_impl, types_mapping
                )
            return created_impl[protocol]

        return __getattribute__

    @classmethod
    def _create_value(
        cls, impl: type, created_impl: dict[type, Any], type_mapping: dict[type, type]
    ) -> Any:
        """
        Создаем значение.
        """
        return_partial = False
        protocol_kwargs = {
            k: v for k, v in get_type_hints(impl.__init__).items() if k != 'return'  # type: ignore
        }
        kwargs: dict[str, Any] = {}
        for k, v in protocol_kwargs.items():
            if v not in type_mapping:
                return_partial = True
            elif v in created_impl:
                kwargs[k] = created_impl[v]
            else:
                created_impl[v] = cls._create_value(
                    type_mapping[v], created_impl, type_mapping
                )
                kwargs[k] = created_impl[v]
        if return_partial:
            return partial(impl, **kwargs)
        return impl(**kwargs)

    @staticmethod
    def create_class_attr(created_class: Any, attr: str) -> None:
        """
        Создаем атрибут класса для внедрения зависимости через FastAPI.
        """

        def inject(request: Request) -> Any:
            if getattr(request.state, 'ioc_container', None) is None:
                request.state.ioc_container = created_class()
            return getattr(request.state.ioc_container, attr)

        setattr(created_class, attr, staticmethod(inject))


class BaseContainer(metaclass=BaseContainerMeta):
    """
    Базовый IoC контейнер.
    """

    ...
