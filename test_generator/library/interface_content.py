from enum import Enum

from schemax_openapi import SchemaData


class InterfaceContent(str, Enum):
    GET = """
    async def $name(self, $params) -> ClientResponse:
        url = self._api_url + f"$path"
        params = {
            **self._actor.params,
            CHANGE_ME_TO_NEED_PARAMS
        }

        return await API.get(url, params=params, headers=self._actor.metadata)
        """
    POST = """
    async def $name(self, $params) -> ClientResponse:
        url = self._api_url + f"$path"
        params = {
            **self._actor.params,
            CHANGE_ME_TO_NEED_PARAMS
        }
        
        data = {
            CHANGE_ME_TO_NEED_BODY
        }

        return await API.post(url, params=params, data=data, headers=self._actor.metadata)
        """
    DELETE = """
    async def $name(self, $params) -> ClientResponse:
        url = self._api_url + f"$path"
        params = {
            **self._actor.params,
            CHANGE_ME_TO_NEED_PARAMS
        }

        return await API.delete(url, params=params, headers=self._actor.metadata)
        """

    @classmethod
    def fill_get_template(cls, schema_data: SchemaData) -> str:
        return (InterfaceContent.GET.replace('$path', schema_data.path)
                                    .replace('$name', schema_data.interface_method)
                                    .replace('$params', ', '.join(schema_data.args)))

    @classmethod
    def fill_post_template(cls, schema_data: SchemaData) -> str:
        return (InterfaceContent.POST.replace('$path', schema_data.path)
                                     .replace('$name', schema_data.interface_method)
                                     .replace('$params', ', '.join(schema_data.args)))

    @classmethod
    def fill_delete_template(cls, schema_data: SchemaData) -> str:
        return (InterfaceContent.DELETE.replace('$path', schema_data.path)
                                       .replace('$name', schema_data.interface_method)
                                       .replace('$params', ', '.join(schema_data.args)))
