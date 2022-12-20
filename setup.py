import setuptools
from codecs import open
from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

# Override standard setuptools commands.
# Enforce the order of dependency installation.
# -------------------------------------------------
PREREQS = ['robotframework',
           'setuptools',
           'RESTinstance',
           'configparser']

from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools.command.egg_info import egg_info


def requires(packages):
    from os import system
    from sys import executable as PYTHON_PATH
    from pkg_resources import require
    require("pip")
    CMD_TMPLT = '"' + PYTHON_PATH + '" -m pip install %s'
    for pkg in packages: system(CMD_TMPLT % (pkg,))


class OrderedInstall(install):
    def run(self):
        requires(PREREQS)
        install.run(self)


class OrderedDevelop(develop):
    def run(self):
        requires(PREREQS)
        develop.run(self)


class OrderedEggInfo(egg_info):
    def run(self):
        requires(PREREQS)
        egg_info.run(self)


CMD_CLASSES = {
    "install": OrderedInstall
    , "develop": OrderedDevelop
    , "egg_info": OrderedEggInfo
}
# -------------------------------------------------

setup(
    name='T24 OFS Robotframework Client Library',
    version='1.0.0',
    description='T24 OFS Library',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Diogo Amaral',
    license='MIT',
    packages=setuptools.find_namespace_packages(),
    setup_requires=['setuptools_scm'],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    cmdclass=CMD_CLASSES,
    install_requires=PREREQS
)
