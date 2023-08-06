import os

from configparser import ConfigParser
from setuptools import setup, find_packages

this_folder = os.path.abspath(os.path.dirname(__file__))


def create_version_py(packagename, version, source_dir='.'):
    package_dir = os.path.join(source_dir, packagename)
    version_py = os.path.join(package_dir, 'version.py')

    version_str = "# This is an automatic generated file please do not edit\n" \
                  "__version__ = '{:s}'".format(version)

    with open(version_py, 'w') as f:
        f.write(version_str)


with open(os.path.join(this_folder, 'README.md')) as f:
    long_description = f.read()


conf = ConfigParser()

conf.read([os.path.join(this_folder, 'setup.cfg')])

metadata = dict(conf.items('metadata'))

PACKAGE_NAME = metadata['package_name']
VERSION = metadata['version']
LICENSE = metadata['license']
DESCRIPTION = metadata['description']
LONG_DESCRIPTION = long_description
LONG_DESCRIPTION_CONTENT_TYPE = 'text/markdown'
AUTHOR = metadata['author']
AUTHOR_EMAIL = metadata['author_email']


setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,
    url='https://github.com/simontorres/simple-version-manager',
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license=LICENSE,
    keywords='version',
    packages=find_packages(),

    entry_points={
        'console_scripts': [
            'vincrement=simple_version_manager.simple_version_manager:run']
    }
)
