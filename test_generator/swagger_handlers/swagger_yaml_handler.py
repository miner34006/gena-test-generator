import os.path
from json import JSONDecodeError
from typing import List

import schemax_openapi
import yaml
from schemax_openapi import SchemaData
from ..library.interface_content import InterfaceContent

from .swagger_handler import SwaggerHandler


class SwaggerYamlHandler(SwaggerHandler):
    format_name = 'swagger_handler_format'

    yaml_file_path: str = None
    interface_file_path: str = None
    schemas_dir_path: str = None

    def __init__(self, yaml_file_path: str, interface_file_path: str, schemas_dir_path: str) -> None:
        super().__init__()
        self.__set_yaml_file(yaml_file_path)
        self.__set_interface_file(interface_file_path)
        self.__set_schemas_dir(schemas_dir_path)

    def read_swagger_data(self) -> List[SchemaData]:
        try:
            with open(self.yaml_file_path, "r") as f:
                if f.name.endswith((".yaml", ".yml")):
                    schema_data_list = schemax_openapi.collect_schema_data(yaml.load(f, yaml.FullLoader))
                else:
                    raise RuntimeError(f"'{f.name}' type is not .json or .yaml file")
                return schema_data_list
        except JSONDecodeError:
            print(f"File '{f.name}' doesn't contain proper JSON")

    def fill_interface_template(self, schema_data: SchemaData) -> str:
        match schema_data.http_method.upper():
            case 'GET':
                return InterfaceContent.fill_get_template(schema_data=schema_data)
            case 'POST':
                return InterfaceContent.fill_post_template(schema_data=schema_data)
            case 'DELETE':
                return InterfaceContent.fill_delete_template(schema_data=schema_data)
            case default:
                raise RuntimeError(f'{schema_data.http_method} is not supported')

    def write_swagger_interface(self, method: str, path: str) -> None:
        print("Generating interfaces from given OpenApi...")

        data_list = self.read_swagger_data()
        data = self.__filter_schema_data_by_path_and_method(data_list, method, path)

        with open(self.interface_file_path, 'a', encoding='utf-8') as file:
            file.write(self.fill_interface_template(data))

        print(f"Successfully interface generated for {method} {path}")

    def __filter_schema_data_by_path_and_method(self, schema_data_list: List[SchemaData], method: str,
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

    def __set_interface_file(self, interface_file_path: str) -> None:
        if not os.path.isfile(interface_file_path):
            raise RuntimeError(f"'{interface_file_path}' doesn't exist")
        self.interface_file_path = interface_file_path

    def __set_schemas_dir(self, schemas_dir_path: str) -> None:
        if not os.path.isdir(schemas_dir_path):
            raise RuntimeError(f"'{schemas_dir_path}' is not dir or doesn't exist")
        self.schemas_dir_path = schemas_dir_path

