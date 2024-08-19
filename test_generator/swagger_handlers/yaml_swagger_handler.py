import os.path

import schemax_openapi
import yaml
from schemax_openapi import SchemaData

from .swagger_handler import SwaggerHandler


class YamlSwaggerHandler(SwaggerHandler):
    format_name = 'swagger_yaml_handler'

    __swagger_file_path: str = ''

    def __init__(self, swagger_file_path: str) -> None:
        super().__init__()
        self.__set_swagger_file_path(swagger_file_path)

    def read_swagger_data(self) -> list[SchemaData]:
        with open(self.__swagger_file_path, "r") as f:
            schema_data_list = schemax_openapi.collect_schema_data(yaml.load(f, yaml.FullLoader))
            return schema_data_list

    def find_data_by_path_and_method(self, schema_data_list: list[SchemaData], path: str, method: str) -> SchemaData:
        path_data_list = list(filter(lambda data: data.path == path.lower(), schema_data_list))
        if len(path_data_list) == 0:
            raise RuntimeError(f"'{path}' doesn't exist")

        method_data_list = list(filter(lambda data: data.http_method == method.lower(), path_data_list))
        if len(method_data_list) == 0:
            raise RuntimeError(f"'{method}' for '{path}' doesn't exist")

        return method_data_list[0]

    def __set_swagger_file_path(self, swagger_file_path: str) -> None:
        if not os.path.isfile(swagger_file_path):
            raise RuntimeError(f"'{swagger_file_path}' doesn't exist")
        self.__swagger_file_path = swagger_file_path
