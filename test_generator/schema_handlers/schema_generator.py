from abc import ABC, abstractmethod

from test_generator.library.gena_data import GenaData


class SchemaGenerator(ABC):
    format_name = 'AbstractSchemaGenerator'

    @abstractmethod
    def generate_response_schema(self, schemas_dir: str, gena_data: GenaData) -> str:
        """
        Генерируем response schema
        """
        ...
