from typing import Union, Tuple, Pattern, Type, Dict, List, Any

from tornado.web import RequestHandler

HandlerType = Union \
[
    Tuple[Union[str, Pattern[str]], Type[RequestHandler]],
    Tuple[Union[str, Pattern[str]], Type[RequestHandler], Dict[str, Any]],
]
HandlerListType = List[HandlerType]
