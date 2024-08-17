from enum import Enum

from schemax_openapi import SchemaData


class InterfaceContent(str, Enum):
    GET = """
    async def $name(self, $params) -> ClientResponse:
        url = self._api_url + f"$path"
        params = {
            **self._actor.params,
            # CHANGE_ME_TO_NEED_PARAMS
        }
        raise NotImplementedError('Need change parameters/body in new generated interface')
        return await API.get(url, params=params, headers=self._actor.metadata)
        """
    POST = """
    async def $name(self, $params) -> ClientResponse:
        url = self._api_url + f"$path"
        params = {
            **self._actor.params,
            # CHANGE_ME_TO_NEED_PARAMS
        }
        
        data = {
            # CHANGE_ME_TO_NEED_BODY
        }
        raise NotImplementedError('Need change parameters/body in new generated interface')
        return await API.post(url, params=params, data=data, headers=self._actor.metadata)
        """
    DELETE = """
    async def $name(self, $params) -> ClientResponse:
        url = self._api_url + f"$path"
        params = {
            **self._actor.params,
            # CHANGE_ME_TO_NEED_PARAMS
        }
        raise NotImplementedError('Need change parameters/body in new generated interface')
        return await API.delete(url, params=params, headers=self._actor.metadata)
        """

    @classmethod
    def fill_template(cls, schema_data: SchemaData) -> str:
        match schema_data.http_method.upper():
            case 'GET':
                func = InterfaceContent.GET
            case 'POST':
                func = InterfaceContent.POST
            case 'DELETE':
                func = InterfaceContent.DELETE
            case default:
                raise RuntimeError(f'{schema_data.http_method} is not supported')
        return (func.replace('$path', schema_data.path)
                    .replace('$name', schema_data.interface_method)
                    .replace('$params', ', '.join(schema_data.args)))
