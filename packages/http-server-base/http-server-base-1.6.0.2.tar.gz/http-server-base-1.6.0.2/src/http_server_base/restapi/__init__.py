from .extras import ArgumentType, ArgumentListType, CanonicalArgumentType, CanonicalArgumentListType, MapperFuncType
from .extras import ArgumentError, ArgumentTypeError, ArgumentValueError, MethodNotAllowedError

from .endpoint import Endpoint

from .irrh import IRest_RequestHandler
from .iirr import IInRequestRouter

from .base_in_request_router import BaseInRequestRouter
from .base_rest_request_handler import BaseRest_RequestHandler

from .regexp_in_request_router import RegexpInRequestRouter
from .regexp_rest_request_handler import RegexpRest_RequestHandler

from .path_tree_in_request_router import PathTreeInRequestRouter
from .path_tree_rest_request_handler import PathTreeRest_RequestHandler

from .prefix_tree_rest_router import PrefixTreeRestRouter

RestRouter = RegexpInRequestRouter
Rest_RequestHandler = RegexpRest_RequestHandler

rest_method = RestRouter.rest_method
extract_args = RestRouter.extract_args
