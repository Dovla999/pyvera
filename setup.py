from setuptools import setup

setup(
    name="silvera-python-generator",
    version="0.1",
    packages=["python_gen"],
    entry_points={
        "silvera_generators": ["python = python_gen.python_generator:python"]
    },
)
