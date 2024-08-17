from abc import ABC, abstractmethod


class SchemaHandler(ABC):
    format_name = 'AbstractSwaggerHandler'

    @abstractmethod
    def add_schema_response_for_method(self, schema_dir_path: str,  method: str, path: str) -> None:
        """
        Генерируем схему для роута в указанный путь
        """
        ...
