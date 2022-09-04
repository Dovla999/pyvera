import os
import warnings
from datetime import datetime
from collections import defaultdict
from jinja2 import Environment, FileSystemLoader

from silvera.generator.registration import GeneratorDesc
from silvera.const import HOST_CONTAINER, HTTP_POST
from silvera.core import (
    CustomType,
    ConfigServerDecl,
    ServiceRegistryDecl,
    ServiceDecl,
    APIGateway,
    TypeDef,
)


def timestamp():
    return "{:%Y-%m-%d %H:%M:%S}".format(datetime.now())


class ServiceGenerator:
    def __init__(self, service: ServiceDecl, output_dir):
        self.service = service
        self.env = self._init_env()
        # self.main_path = csharp_struct(output_dir, service.name)

    def _init_env(self):
        pass

    def generate_model(self):
        pass

    def generate(self):
        for typedef in self.service.api.typedefs:
            # print(typedef)
            print([f for f in typedef.fields])


def generate_service(service, output_dir):
    generator = ServiceGenerator(service, output_dir)
    generator.generate()


def generate_service_registry():
    pass


def generate_api_gateway():
    pass


_obj_to_fnc = {
    # ConfigServerDecl: generate_config_server,
    ServiceRegistryDecl: generate_service_registry,
    ServiceDecl: generate_service,
    APIGateway: generate_api_gateway,
}


def generate(decl, output_dir, debug):
    """Entry point function for code generator.

    Args:
        decl(Decl): can be declaration of service registry or config
                    server.
        output_dir(str): output directory.
        debug(bool): True if debug mode activated. False otherwise.
    """

    print("Called!")
    print(decl, output_dir)
    fnc = _obj_to_fnc[decl.__class__]
    fnc(decl, output_dir)
    pass


python = GeneratorDesc(
    language_name="python",
    language_ver="3.10",
    description="Python 3.10 code generator",
    gen_func=generate,
)
