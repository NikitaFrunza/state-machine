from setuptools import find_packages
from setuptools import setup

setup(
    name='yasmin_viewer',
    version='2.3.1',
    packages=find_packages(
        include=('yasmin_viewer', 'yasmin_viewer.*')),
)
