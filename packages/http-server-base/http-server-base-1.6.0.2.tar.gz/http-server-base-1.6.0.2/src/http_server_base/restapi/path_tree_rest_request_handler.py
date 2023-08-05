from . import BaseRest_RequestHandler, PathTreeInRequestRouter

class PathTreeRest_RequestHandler(BaseRest_RequestHandler):
    in_request_router_class = PathTreeInRequestRouter
