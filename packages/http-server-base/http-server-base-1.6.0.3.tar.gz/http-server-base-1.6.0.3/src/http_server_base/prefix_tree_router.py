from typing import Union, Type, Any, Dict, Optional, Tuple

# noinspection PyCompatibility
from dataclasses import dataclass, field, InitVar, replace

from tornado.httputil import HTTPServerRequest, HTTPMessageDelegate
from tornado.web import RequestHandler

from . import  Handler, IRouter
from .tools import PrefixTreeMap, RegExpType

@dataclass
class PrefixTreeRouter(IRouter):
    tree: PrefixTreeMap[Handler] = field(init=False, default_factory=PrefixTreeMap)
    optimize_tree: InitVar[bool] = False
    last_key: str = field(init=False, repr=False, default=None)
    last_value: Optional[Handler] = field(init=False, repr=False, default=None)
    
    def __post_init__(self, optimize_tree: bool):
        for h in self.app.handlers:
            self.add_handler(*h)
        
        if (optimize_tree):
            self.optimize()
    
    def add_handler(self, pattern: Union[str, bytes, RegExpType], handler_type: Type[RequestHandler], *params, **kwargs) -> Handler:
        if (isinstance(pattern, RegExpType)):
            pattern = pattern.pattern
        if (isinstance(pattern, bytes)):
            pattern = pattern.decode()
        handler = Handler(handler_type, *params)
        self._register_handler(pattern, handler)
        return handler
    
    def _register_handler(self, key: str, handler: Handler):
        key = key.rstrip(self.tree.separator)
        handler.match_args.insert(0, key)
        self.tree.add(key, handler)
        self.last_key = None
    
    def optimize(self):
        self.tree.optimize()
    
    def get_key(self, request: HTTPServerRequest, **kwargs) -> str:
        return request.path
    
    def _match(self, request: HTTPServerRequest, **kwargs) -> Optional[Handler]:
        key = self.get_key(request, **kwargs)
        if (key == self.last_key):
            return self.last_value
        
        result = self.tree.get(key, None)
        print(f"Matching path '{key}' => {result}")
        self.last_value = result
        if (result is not None):
            _sep = self.tree.separator
            offset = _sep.join(key.split(_sep)[len(result.match_args[0].split(_sep)):])
            # noinspection PyArgumentList
            result: Handler = replace(result, match_args=[ offset, *result.match_args[1:] ])
        return result
