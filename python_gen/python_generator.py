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
from silvera.core import TypedList, TypeDef, TypedSet, TypedDict


def get_root_path():
    """Returns project's root path."""
    path = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
    return path


def get_templates_path():
    """Returns the path to the templates folder."""
    return os.path.join(get_root_path(), "python_gen", "templates")


def timestamp():
    return "{:%Y-%m-%d %H:%M:%S}".format(datetime.now())


def first_upper(string):
    return string[0].upper() + string[1:]


def first_lower(string):
    return string[0].lower() + string[1:]


def convert_type(_type):
    def _convert_type(_type):
        if isinstance(_type, TypeDef):
            return first_upper(_type.name)
        if isinstance(_type, TypedList):
            return f"List[{_convert_type(_type.type)}]"
        if isinstance(_type, TypedSet):
            return f"Set[{_convert_type(_type.type)}]"
        if isinstance(_type, TypedDict):
            return f"Dict[{_convert_type(_type.key_type)}, {_convert_type(_type.value_type)}]"
        return _type

    return _convert_type(_type)


def silvera_type_to_pydantic(field_type):
    primitives_map = {
        "date": "date",
        "int": "int",
        "float": "float",
        "double": "float",
        "str": "str",
        "list": "list",
        "set": "set",
        "dict": "dict",
    }
    return (
        primitives_map[field_type]
        if field_type in primitives_map
        else convert_type(field_type)
    )


class ServiceGenerator:
    def __init__(self, service: ServiceDecl, output_dir):
        self.service = service
        self.env = self._init_env()

    def _init_env(self):
        env = Environment(loader=FileSystemLoader(get_templates_path()))

        env.filters["first_upper"] = first_upper
        env.filters["first_lower"] = first_lower
        env.filters["silvera_type_to_pydantic"] = lambda t: silvera_type_to_pydantic(t)
        env.globals["service_name"] = self.service.name
        env.globals[
            "header"
        ] = lambda: f"\n\tGenerated by: silvera\n\tDatetime: {datetime.now()}\n"

        return env

    def generate_model(self):
        for typedef in self.service.api.typedefs:
            class_template = self.env.get_template("model.j2")
            if not os.path.exists("models"):
                os.makedirs("models")
            class_template.stream({"typedef": typedef}).dump(
                os.path.join("models", typedef.name + ".py")
            )

    def generate(self):
        self.generate_model()


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
