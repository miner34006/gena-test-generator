import os
from dataclasses import dataclass, field

import schemax_openapi
import yaml
from district42 import GenericSchema
from schemax_openapi import SchemaData


@dataclass
class GenaData:
    http_method: str
    api_path: str

    interface_method: str

    args: list[str]
    queries: list[str]

    response_schema_name: str
    response_schema: GenericSchema


def get_gena_data_for_method_and_path(yaml_file_path: str, method_route: str, path_route: str) -> GenaData:
    with open(yaml_file_path, "r") as f:
        schema_data_list = schemax_openapi.collect_schema_data(yaml.load(f, yaml.FullLoader))

    path_data_list = list(filter(lambda data: data.path == path_route.lower(), schema_data_list))
    if len(path_data_list) == 0:
        raise RuntimeError(f"'{path_route}' doesn't exist")

    method_data_list = list(filter(lambda data: data.http_method == method_route.lower(), path_data_list))
    if len(method_data_list) == 0:
        raise RuntimeError(f"'{method_route}' for '{method_route}' doesn't exist")

    schema: SchemaData = method_data_list[0]

    return GenaData(
        http_method=schema.http_method,
        api_path=schema.path,
        interface_method=schema.interface_method,
        args=schema.args,
        queries=schema.queries,
        response_schema_name=schema.schema_prefix,
        response_schema=schema.response_schema_d42
    )
