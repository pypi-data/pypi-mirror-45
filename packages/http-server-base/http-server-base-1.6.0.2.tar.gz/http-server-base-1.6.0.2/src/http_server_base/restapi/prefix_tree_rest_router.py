from typing import Union, Type, Any, Dict, Optional

from http_server_base import Handler, PrefixTreeRouter
from http_server_base.tools import RegExpType
from . import BaseRest_RequestHandler, IRest_RequestHandler

class PrefixTreeRestRouter(PrefixTreeRouter):
    def add_handler(self, *params, **kwargs) -> Handler:
        x, *other = params
        if (isinstance(x, (str, RegExpType))):
            t, *other = other
        else:
            t = x
        
        print("Trying to add REST handler...")
        if (isinstance(t, type) and issubclass(t, IRest_RequestHandler)):
            return self.add_rest_handler(t, *other, **kwargs)
        else:
            return super().add_handler(*params, **kwargs)
    
    def add_rest_handler(self, handler_type: Type[IRest_RequestHandler], *params, **kwargs) -> Handler:
        if (not issubclass(handler_type, BaseRest_RequestHandler)):
            raise TypeError("IRest_RequestHandler subclasses other than BaseRest_RequestHandler are not supported")
        print(f"Adding REST handler: '{handler_type}'")
        handler_type: Type[BaseRest_RequestHandler]
        
        handler = Handler(handler_type, *params)
        base_path = handler_type.base_path.rstrip('/')
        for _, path in handler_type.in_request_router_class.get_class_endpoints(handler_type):
            path = base_path + path
            print(f"Registering endpoint '{path}'")
            self._register_handler(path, handler)
        
        return handler
