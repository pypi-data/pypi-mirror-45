from . import BaseInRequestRouter, Endpoint
from http_server_base.tools import PrefixTreeMap, PathTreeMap

class PathTreeInRequestRouter(BaseInRequestRouter[PathTreeMap, str]):
    mapper_type = PathTreeMap[Endpoint[str]]
