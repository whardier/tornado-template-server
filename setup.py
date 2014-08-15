# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

from tornado_template_server import __version__, __author__, __author_email__, __description__, __license__

setup(
    name='tornado_template_server',
    version=__version__,
    author=__author__,
    author_email=__author_email__,
    description=__description__,
    license=__license__,
    packages=["tornado_template_server"],
    install_requires=[
        'tornado',
        'tornado_data_uri',
    ],
    entry_points={
        'console_scripts': [
            'tornado-template-server = tornado_template_server.__main__:run',
        ],
    }
)
