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

    def _find_variables(self, file_content: str) -> dict:
        # variables are stored in double **, so we need to find them
        # for example: **Variable** = value
        variables = {}
        for line in file_content.split('\n'):
            if line.startswith('**') and '=' in line:
                key, value = line.split('=', 1)
                key = key.replace('**', '').strip()
                variables[key] = value.strip()
        return variables
