from .md_handler import MdHandler
from .md_list_handler import MdListHandler
from .md_table_handler import MdTableHandler

__all__ = ['MdHandler', 'MdListHandler', 'MdTableHandler']


def get_md_handlers() -> list[MdHandler]:
    return [f() for f in MdHandler.__subclasses__()]  # type: ignore


def get_md_handler_by_name(name: str) -> MdHandler:
    return [h for h in get_md_handlers() if h.format_name == name][0]


def get_default_md_handler() -> MdHandler:
    return MdListHandler()
