import schemax_openapi
import yaml
from schemax_openapi import SchemaData


def read_swagger_data(yaml_file_path: str) -> list[SchemaData]:
    with open(yaml_file_path, "r") as f:
        return schemax_openapi.collect_schema_data(yaml.load(f, yaml.FullLoader))


def filter_schema_data_by_path_and_method(schema_data_list: list[SchemaData], method: str,
                                          path: str) -> SchemaData:

    path_data_list = list(filter(lambda data: data.path == path.lower(), schema_data_list))
    if not path_data_list:
        raise RuntimeError(f"'{path}' doesn't exist")

    method_data_list = list(filter(lambda data: data.http_method == method.lower(), path_data_list))
    if not method_data_list:
        raise RuntimeError(f"'{method}' for '{path}' doesn't exist")

    return method_data_list[0]
