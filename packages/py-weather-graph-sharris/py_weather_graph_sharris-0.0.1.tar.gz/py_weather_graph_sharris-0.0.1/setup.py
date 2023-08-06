import os
from setuptools import setup

from weather_graph import name, version


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


packages = ['weather_graph', 'tests']
setup(
    name=name,
    version=version,
    author='Stephanie Harris',
    author_email='sharris@eastern.edu',
    description='Plot Graph of Local Weather Patterns',
    license='MIT',
    keywords='weather graph matplotlib',
    url='https://github.com/Steph-harris/py_weather_graph',
    package=packages,
    long_description=read('README.md'),
)
