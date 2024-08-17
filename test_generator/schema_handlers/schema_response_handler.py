import os.path
from test_generator.helpers.swagger_helpers import read_swagger_data, filter_schema_data_by_path_and_method

from .schema_handler import SchemaHandler


class SchemaResponseHandler(SchemaHandler):
    format_name = 'social_interface'

    yaml_file_path: str = None

    def __init__(self, yaml_file_path: str) -> None:
        super().__init__()
        self.__set_yaml_file(yaml_file_path)

    def add_schema_response_for_method(self, schema_dir_path: str, method: str, path: str) -> None:
        if not os.path.isdir(schema_dir_path):
            raise RuntimeError(f"'{schema_dir_path}'dir doesn't exist or is a not dir")
        print("Generating response schema from given OpenApi...")

        data_list = read_swagger_data(self.yaml_file_path)
        data = filter_schema_data_by_path_and_method(data_list, method, path)
        schema_file = f'{schema_dir_path}/{data.interface_method}.py'

        with open(schema_file, 'a') as file:
            file.write(f'from d42 import optional, schema\n\n\n\n{data.schema_prefix} = {data.response_schema_d42}')

        print(f"Successfully response schema generated for {method} {path} in {schema_file}")

    def __set_yaml_file(self, yaml_file_path: str) -> None:
        if not os.path.isfile(yaml_file_path):
            raise RuntimeError(f"'{yaml_file_path}' doesn't exist")
        self.yaml_file_path = yaml_file_path
