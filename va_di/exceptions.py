"""
Модуль, содержащий исключения.
"""


class InvalidContainerError(Exception):
    """
    Ошибка, возникающая при неправильных настройках контейнера.
    """

    def __init__(self, message: str, *args: object) -> None:
        super().__init__(*args)
        self.message = message

    def __str__(self) -> str:
        return self.message
