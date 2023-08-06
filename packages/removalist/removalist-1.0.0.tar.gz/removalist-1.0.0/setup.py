
from setuptools import setup, find_packages
from removalist.core.version import get_version

VERSION = get_version()

f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name='removalist',
    version=VERSION,
    description='Add Dependencies and Extensions for Hashicorp Packer',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Bruno Briante',
    author_email='bruno.briante@convenia.com.br',
    url='https://github.com/convenia/removalist',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    package_data={'removalist': ['templates/*']},
    include_package_data=True,
    entry_points="""
        [console_scripts]
        removalist = removalist.main:main
    """,
)
