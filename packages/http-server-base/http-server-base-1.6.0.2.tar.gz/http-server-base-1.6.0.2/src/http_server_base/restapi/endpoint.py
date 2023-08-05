from typing import List, Callable, Tuple, Any, Generic, TypeVar, Awaitable, Dict
# noinspection PyCompatibility
from dataclasses import dataclass, field

from . import CanonicalArgumentListType

T = TypeVar('T')
@dataclass
class Endpoint(Generic[T]):
    name: str
    method: str
    key: T
    path: str
    paths: Tuple[str, T]
    
    query_arguments: CanonicalArgumentListType
    body_arguments: CanonicalArgumentListType
    path_arguments: CanonicalArgumentListType
    header_arguments: CanonicalArgumentListType
    arguments: Dict[str, CanonicalArgumentListType] = field(init=False)
    
    action: Callable[[Any], Awaitable[Any]] = field(repr=False, default=None)
    extra_args: Dict[str, Any] = field(repr=False, default_factory=dict)
    
    def __post_init__(self):
        self.arguments = { s: getattr(self, f'{s}_arguments') for s in self.arguments_sources }
    
    @property
    def arguments_sources(self) -> List[str]:
        return [ 'query', 'body', 'path', 'header' ]
