from . import BaseRest_RequestHandler, RegexpInRequestRouter

class RegexpRest_RequestHandler(BaseRest_RequestHandler):
    in_request_router_class = RegexpInRequestRouter
