from abc import ABC, abstractmethod

from test_generator.library.suite import Suite


class MdHandler(ABC):
    format_name = 'AbstractMdHandler'

    @abstractmethod
    def read_data(self, file_path: str, *args, **kwargs) -> Suite:
        """
        Читаем данные из файла сценариев, парсим и отдаем Suite
        """
        ...

    @abstractmethod
    def write_data(self, file_path: str, data: Suite, force: bool, *args, **kwargs) -> None:
        """
        Записываем list сценариев в файл и всю meta информацию
        """
        ...

    def validate_scenarios(self, file_path: str, *args, **kwargs) -> None:
        """
        Проверяем сценарии на валидность
        """
        ...
