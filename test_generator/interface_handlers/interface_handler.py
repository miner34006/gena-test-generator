from abc import ABC, abstractmethod

from schemax_openapi import SchemaData


class InterfaceHandler(ABC):
    format_name = 'AbstractInterfaceHandler'

    @abstractmethod
    def add_api_method_to_interface(self, data: SchemaData) -> None:
        """
        Извлекаем данные из data и добавляем интерфейс в файл интерфейса
        """
        ...

