import setuptools
from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools.command.egg_info import egg_info
from setuptools import setup
import time


class CustomInstallCommand(install):
    def run(self):
        print("Installing pkg... Will take about 360 seconds")
        time.sleep(360)
        install.run(self)


class CustomDevelopCommand(develop):
    def run(self):
        develop.run(self)


class CustomEggInfoCommand(egg_info):
    def run(self):
        egg_info.run(self)

setup(
    name="simulating-pkg-taking-6mins-to-install",
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