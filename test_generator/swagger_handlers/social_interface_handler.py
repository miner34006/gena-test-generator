import os.path

import schemax_openapi
import yaml
from schemax_openapi import SchemaData

from ..library.interface_content import InterfaceContent
from .swagger_handler import SwaggerHandler


class SocialInterfaceHandler(SwaggerHandler):
    format_name = 'social_interface'

    yaml_file_path: str = ''

    def __init__(self, yaml_file_path: str) -> None:
        super().__init__()
        self.__set_yaml_file(yaml_file_path)

    def add_api_method_to_interface(self, interface_file_path: str, method: str, path: str) -> None:
        if not os.path.isfile(interface_file_path):
            raise RuntimeError(f"'{interface_file_path}' doesn't exist")
        print("\nGenerating interfaces from given OpenApi...")

        data_list = self.__read_swagger_data()
        data = self.__filter_schema_data_by_path_and_method(data_list, method, path)

        with open(interface_file_path, 'r', encoding='utf-8') as file:
            if f"def {data.interface_method}(" in file.read():
                print(f"Method {data.interface_method} already exists in {interface_file_path}, skipping...")
                return

        with open(interface_file_path, 'a', encoding='utf-8') as file:
            file.write(InterfaceContent.fill_template(data))

        print(f"{method} {path} interface was generated in {interface_file_path}")

    def __read_swagger_data(self) -> list[SchemaData]:
        with open(self.yaml_file_path, "r") as f:
            schema_data_list = schemax_openapi.collect_schema_data(yaml.load(f, yaml.FullLoader))
            return schema_data_list

    def __filter_schema_data_by_path_and_method(self, schema_data_list: list[SchemaData], method: str,
                                                path: str) -> SchemaData:
        path_data_list = list(filter(lambda data: data.path == path.lower(), schema_data_list))

        if len(path_data_list) == 0:
            raise RuntimeError(f"'{path}' doesn't exist")

        method_data_list = list(filter(lambda data: data.http_method == method.lower(), path_data_list))
        if len(method_data_list) == 0:
            raise RuntimeError(f"'{method}' for '{path}' doesn't exist")

        return method_data_list[0]

    def __set_yaml_file(self, yaml_file_path: str) -> None:
        if not os.path.isfile(yaml_file_path):
            raise RuntimeError(f"'{yaml_file_path}' doesn't exist")
        self.yaml_file_path = yaml_file_path
