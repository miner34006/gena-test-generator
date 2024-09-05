from abc import ABC, abstractmethod

from test_generator.library.gena_data import GenaData


class ApiGenerator(ABC):
    format_name = 'AbstractApiGenerator'

    @abstractmethod
    def add_api_method(self, file_path: str, gena_data: GenaData) -> str:
        """
        Генерируем api интерфейс
        """
        ...
