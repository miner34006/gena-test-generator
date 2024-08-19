from abc import ABC, abstractmethod


class ApiGenerator(ABC):
    format_name = 'AbstractApiGenerator'

    @abstractmethod
    def add_api_method(self, file_path: str,  method: str, path: str) -> str:
        """
        Генерируем api интерфейс
        """
        ...
