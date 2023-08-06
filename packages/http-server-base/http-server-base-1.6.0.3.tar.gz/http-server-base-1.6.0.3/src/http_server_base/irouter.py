from logging import getLogger
from typing import Type, Any, Dict, Union, Optional, List, Tuple

# noinspection PyCompatibility
from dataclasses import dataclass, field
from tornado.httputil import HTTPServerRequest, HTTPMessageDelegate

from tornado.routing import Router, Rule, Matcher, RuleRouter
from tornado.web import RequestHandler

from http_server_base import HandlerType
from . import IApplication, ILoggable
from .tools import RegExpType

@dataclass
class Handler:
    handler_type: Type[RequestHandler]
    params: Dict[str, Any] = field(default_factory=dict)
    match_args: List[Any] = field(default_factory=list)

@dataclass
class IRouter(RuleRouter, Rule, Matcher, ILoggable):
    app: IApplication
    name: str = None
    
    logger_name: str = None
    def __post_init__(self):
        if (self.logger_name is None):
            self.logger_name = f'{self.app.logger_name}.router'
        self.logger = getLogger(self.logger_name)
    
    def add_rules(self, rules: List[HandlerType], **kwargs):
        for pattern, handler, *params in rules:
            self.add_handler(pattern, handler, *params, **kwargs)
    def add_handler(self, pattern: Union[str, bytes, RegExpType], handler_type: Type[RequestHandler], *params, **kwargs) -> Handler:
        pass
    
    @property
    def matcher(self):
        return self
    @property
    def target(self):
        return self
    
    def match(self, request: HTTPServerRequest, **kwargs) -> Optional[Dict[str, Any]]:
        m = self._match(request, **kwargs)
        if (m is not None):
            return m.params
    
    def find_handler(self, request: HTTPServerRequest, **kwargs) -> Optional[HTTPMessageDelegate]:
        m = self._match(request, **kwargs)
        if (m is not None):
            args = m.match_args
            if (args is None):
                args = [ request.path.encode() ]
            return self.app.get_handler_delegate(request, target_class=m.handler_type, target_kwargs=m.params, path_args=args)
    
    def _match(self, request: HTTPServerRequest, **kwargs) -> Optional[Handler]:
        raise NotImplementedError
