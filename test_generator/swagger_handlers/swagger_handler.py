from abc import ABC, abstractmethod
from typing import List

from schemax_openapi import SchemaData


class SwaggerHandler(ABC):
    format_name = 'AbstractSwaggerHandler'
    template_content = ''

    @abstractmethod
    def read_swagger_data(self, file_path: str, *args, **kwargs) -> List[SchemaData]:
        """
        Читаем данные из файла swagger-а
        """
        ...

    @abstractmethod
    def write_swagger_interface(self, interface_dir: str, file_path: str, method: str, path: str) -> None:
        """
        Генерируем примерный интерфейс в *Api.py
        """
        ...

    @abstractmethod
    def fill_interface_template(self, schema_data: SchemaData) -> str:
        """
        Наполняем шаблон интерфейса из данных SchemaData
        """
