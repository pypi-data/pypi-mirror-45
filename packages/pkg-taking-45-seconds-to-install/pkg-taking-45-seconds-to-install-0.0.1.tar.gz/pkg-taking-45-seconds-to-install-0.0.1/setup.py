import setuptools
from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools.command.egg_info import egg_info
from setuptools import setup
import os
import time


def custom_command():
    import sys
    if sys.platform in ['darwin', 'linux']:
        os.system('./custom_command.sh')


class CustomInstallCommand(install):
    def run(self):
        print("Installing pkg... Will take about 45 seconds")
        time.sleep(45)
        install.run(self)


class CustomDevelopCommand(develop):
    def run(self):
        develop.run(self)


class CustomEggInfoCommand(egg_info):
    def run(self):
        egg_info.run(self)

setup(
    name="pkg-taking-45-seconds-to-install",
    version="0.0.1",
    author="yb",
    author_email="ykim828@hotmail.com",
    description="A small example package",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    cmdclass={
        'install': CustomInstallCommand,
        'develop': CustomDevelopCommand,
        'egg_info': CustomEggInfoCommand,
    },
)