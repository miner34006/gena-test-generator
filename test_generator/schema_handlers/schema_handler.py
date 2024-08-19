from abc import ABC, abstractmethod

from schemax_openapi import SchemaData


class SchemaHandler(ABC):
    format_name = 'AbstractSchemaHandler'

    @abstractmethod
    def add_schema_response(self, schema_data: SchemaData) -> None:
        """
        Генерируем d42 response схему для SchemaData
        """
        ...
