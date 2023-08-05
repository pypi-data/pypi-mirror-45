# noinspection PyCompatibility
from dataclasses import dataclass, field

from . import HandlerListType
from . import IApplication, IHandlerController

@dataclass
class HandlerController(IHandlerController):
    base_path: str = field(init=False, repr=False)
    application: IApplication = None
    handlers: HandlerListType = field(default_factory=list)
    
    def get_handlers_for(self, host: str) -> HandlerListType:
        getter = getattr(self, f'get_{host}_handlers', None)
        if (getter is None):
            return list()
        else:
            return getter()
    
    def get_self_handlers(self) -> HandlerListType:
        return self.handlers
