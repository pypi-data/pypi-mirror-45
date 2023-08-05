from . import HandlerListType

class IHandlerController:
    base_path: str
    handlers: HandlerListType
    
    def get_handlers_for(self, host: str) -> HandlerListType:
        pass
