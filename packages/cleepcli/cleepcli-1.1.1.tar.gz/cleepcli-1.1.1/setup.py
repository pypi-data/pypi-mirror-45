try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from cleepcli.config import VERSION

setup(
    name = 'cleepcli',
    version = VERSION,
    description = 'Cleep-cli helps developers to build great Cleep applications from command line.',
    author = 'Tanguy Bonneau',
    author_email = 'tanguy.bonneau@gmail.com',
    maintainer = 'Tanguy Bonneau',
    maintainer_email = 'tanguy.bonneau@gmail.com',
    url = 'http://www.github.com/tangb/cleep-cli/',
    packages = ['cleepcli'],
    include_package_data = True,
    install_requires = ['Click>=7.0,<8.0', 'watchdog>=0.9.0,<1.0.0', 'requests>=2.21.0,<3.0.0', 'coverage>=4.5.3,<5.0.0'],
    scripts = ['bin/cleep-cli']
)
