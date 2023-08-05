import re
import socket
from logging import getLogger
from typing import *

# noinspection PyCompatibility
from dataclasses import dataclass, field, asdict, InitVar, fields, Field

from tornado.httpserver import HTTPServer
from tornado.httputil import HTTPServerRequest, HTTPMessageDelegate
from tornado.ioloop import IOLoop
from tornado.routing import HostMatches, Rule, RuleRouter, ReversibleRuleRouter, AnyMatches, Matcher
from tornado.web import _ApplicationRouter as ApplicationRouter

from . import HandlerType
from . import IApplication, IHandlerController
from .tools import RegExpType, ExtendedLogger, ConfigLoader

@dataclass
class Host:
    application: IApplication
    name: str
    protocol: str = 'http'
    port: int = None
    address: str = None
    bind_address: str = ''
    
    pattern: Union[str, RegExpType] = None
    matcher: Matcher = None
    router_class: Type[RuleRouter] = ApplicationRouter
    router: RuleRouter = None
    rule: Rule = None
    
    def __post_init__(self):
        if (self.port is None):
            self.port = 443 if (self.protocol == 'https') else 80
        
        if (self.address is None):
            settings = None
            if (self.application is not None):
                settings = self.application.settings
            if (settings is None):
                settings = dict()
            
            self.address = settings.get(f'{self.name}_address')
            if (self.address is None):
                get_host_func = getattr(self.application, f'get_{self.name}_host', None)
                if (get_host_func is not None and callable(get_host_func)):
                    _host = get_host_func()
                    if (isinstance(_host, tuple) and len(_host) == 2):
                        listen_address, host_pattern = _host
                    else:
                        listen_address = _host
                else:
                    listen_address = \
                        settings.get('listen_address') \
                        or settings.get('listen_ip') \
                        or settings.get('ip') \
                        or socket.gethostbyname(socket.gethostname()) \
                
                self.address = f"{self.protocol}://{listen_address}:{self.port}"
                
        
        if (self.pattern is None):
            self.pattern = re.escape(self.bind_address)
        
        if (self.matcher is None):
            self.matcher = HostMatches(self.pattern) if (self.pattern) else AnyMatches()
        
        if (self.router is None):
            self.router = self.router_class(self.application)
        
        if (self.rule is None):
            self.rule = Rule(self.matcher, target=self.router, name=f"Host:{self.name}")

@dataclass
class ApplicationBase2(IApplication):
    hosts: List[Host] = None
    # bind_address: str = None
    # new_format_access_log:  bool = False
    
    internal_router_class: Type[RuleRouter] = ApplicationRouter
    router: ReversibleRuleRouter = None
    
    listen_port: InitVar[int] = 80
    use_default_host: bool = True
    default_host: Host = field(repr=False, default=None)
    default_host_name: InitVar[str] = 'self'
    
    logger_name: str = 'http_server'
    access_logger_name:  str = None
    access_logger: Optional[ExtendedLogger] = field(repr=False, default=None)
    
    _hosts_map: Dict[str, Host] = field(init=False, repr=False, default_factory=dict)
    server: HTTPServer = field(init=False, repr=False, default=None)
    
    config_priority: InitVar[bool] = False
    config_name: InitVar[str] = 'main'
    config_prefix: InitVar[str] = 'HTTP'
    extra_settings: InitVar[Dict[str, Any]] = None
    prevent_config_load: InitVar[bool] = False
    
    def __post_init__(self, listen_port: int, default_host_name: str, config_priority: bool, config_name: str, config_prefix: str, extra_settings: Dict[str, Any], prevent_config_load: bool, **kwargs):
        # Settings
        if (not prevent_config_load):
            if (extra_settings is None):
                extra_settings = dict()
            extra_settings.update(kwargs)
            self.settings: Dict[str, Any] = ConfigLoader.get_from_config(config_prefix, config_name, default=dict())
            self.settings.update(extra_settings)
            self.settings.setdefault('listen_port', self.settings.pop('port', None))
            
            _s = dict()
            priorities: List[Dict[str, Any]] = [ self.__dict__, self.settings ]
            if (config_priority):
                priorities = reversed(priorities)
            for p in priorities:
                _s.update(p)
            allowed_fields: List[str] = list(f.name for f in fields(self) if f.init) + [ 'listen_port', 'default_host_name' ]
            _s = { k: v for k, v in _s.items() if k in allowed_fields }
            self.__init__(**_s, prevent_config_load=True)
            self.settings.update(_s)
            return
        
        self.logger = getLogger(self.logger_name)
        if (self.access_logger_name is not None and self.access_logger is None):
            self.access_logger = getLogger(self.logger_name)
        
        # Routers
        if (self.router is None):
            self.router = ReversibleRuleRouter()
        
        # Hosts
        if (self.hosts is None):
            _hosts = list()
        else:
            _hosts = list(self.hosts)
        self.hosts = list()
        if (self.use_default_host):
            if (self.default_host is None):
                self.default_host = Host(self, default_host_name, port=listen_port, bind_address='', router_class=self.internal_router_class)
            self.add_host(self.default_host)
        for host in _hosts:
            self.add_host(host)
        
        # Handlers
        if (isinstance(self.handlers, dict)):
            for host, handlers in self.handlers.items():
                self.add_handlers(handlers, host)
        else:
            self.add_handlers(self.handlers)
        for controller in self.handler_controllers:
            self.attach_handler_controller(controller)
        
        # Other
        _def_host = self.default_host
        super(IApplication, self).__init__(**self.settings)
        self.default_host = _def_host
        self.server = HTTPServer(self)
    
    #region Hosts and Handlers
    def add_host(self, host: Union[Host, str, dict]):
        if (isinstance(host, Host)):
            host.application = self
            host.router.application = self
        elif (isinstance(host, str)):
            host = Host(self, host, router_class=self.internal_router_class)
        elif (isinstance(host, tuple)):
            host = Host(self, *host, router_class=self.internal_router_class)
        elif (isinstance(host, dict)):
            host.setdefault('router_class', self.internal_router_class)
            host = Host(self, **host)
        else:
            raise ValueError(f"Invalid host argument: '{host}' (type: {type(host)})")
        
        self.logger.info(f"Adding host '{host.name}': {host}")
        self.router.rules.insert(0, host.rule)
        self.hosts.append(host)
        self._hosts_map[host.name] = host
    
    def find_handler(self, request: HTTPServerRequest, **kwargs) -> Optional[HTTPMessageDelegate]:
        return self.router.find_handler(request, **kwargs)
    
    def add_handlers(self, handlers: List[Union[Rule, HandlerType]], host: str = None):
        added = False
        if (host is not None):
            if (host not in self._hosts_map):
                raise ValueError(f"Host '{host}' is not registered")
            self._hosts_map[host].router.add_rules(handlers)
            added = True
        if (self.use_default_host):
            self.default_host.router.add_rules(handlers)
            added = True
        
        if (not added):
            self.logger.warning("No handlers were added by add_handlers() due to the invalid configuration (neither host nor default router were configured)")
    
    def attach_handler_controller(self, controller: IHandlerController):
        for host in self.hosts:
            self.add_handlers(controller.get_handlers_for(host.name), host.name)
    #endregion
    
    #region Start server
    def start_listening(self):
        for host in self.hosts:
            self.logger.info(f"{self.name}: Listening on the {host.name} host: {host.address} (bind address='{host.bind_address}', port={host.port})")
            self.server.listen(host.port, host.bind_address)
    
    def run(self, blocking=True, num_processes=1):
        """
        Runs the server on the port specified earlier.
        Server blocks the IO.
        """
        
        self.logger.info(f"{self.name}: Starting HTTP service...")
        self.start_listening()
        self.server.start(num_processes=num_processes)
        self.logger.info(f"{self.name}: Service started")
        
        if (blocking):
            IOLoop.current().start()
    
    @classmethod
    def simple_start_prepare(cls):
        from logging import getLogger
        from http_server_base.tools import setup_logging
        
        # Configure logger
        setup_logging()
        logger = getLogger(cls.logger_name)
        logger.setLevel('TRACE')
        logger.info("Logger started")
        ConfigLoader.load_configs(soft_mode=True)
        
        return logger
    
    @classmethod
    def _simple_start_func(cls, pre_run_func: Union[Callable[['ApplicationBase2'], None], None], num_processes=1, blocking=True, **settings) -> Tuple[Union['ApplicationBase2', None], Union[Exception, None]]:
        """
        If any expected error occurs, returns the instance of initialized class (if any) and the exception
        
        :param pre_run_func:
        Function to be run after the server initialization but before actual start.
        Must take only one argument - the server instance.
        :param settings:
        Settings used for the server initialization
        :return:
        Tuple:
         - instance of initialized object (if any)
         - exception info
        """
        
        server_application: ApplicationBase2 = cls(**settings)
        if (callable(pre_run_func)):
            pre_run_func(server_application)
        
        try:
            server_application.run(num_processes=num_processes, blocking=blocking)
        except KeyboardInterrupt:
            server_application.logger.info("Keyboard interrupt. Exiting now.")
        except PermissionError as e:
            return server_application, e
        
        return None, None
    
    @classmethod
    def simple_start_server(cls, pre_run_func: Union[Callable[['ApplicationBase2'], None], None] = None, **settings):
        """
        Initializes logging and ConfigLoader in the soft-mode,
        than initializes the class instance, runs this function and starts the server.
        
        :param pre_run_func:
        Function to be run after the server initialization but before actual start.
        Must take only one argument - the server instance.
        :param settings:
        Settings used for the server initialization
        :return:
        """
        
        logger = cls.simple_start_prepare()
        
        try:
            server_application, exception = cls._simple_start_func(pre_run_func, **settings)
            
            if (isinstance(exception, PermissionError)):
                server_application.logger.error("Permission error. Restarting server with the port of range 8xxx.")
                new_port = server_application.default_host.port + 8000
                del server_application
                settings['listen_port'] = new_port
                logger.info(f"Restarting server on the port {new_port}.")
                cls._simple_start_func(pre_run_func, **settings)
        
        except Exception:
            logger.exception(msg="Unhandled exception while starting server:")
            raise
    #endregion
