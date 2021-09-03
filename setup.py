import io
import os
import re

from setuptools import find_packages
from setuptools import setup


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u'')
    with io.open(filename, mode='r', encoding='utf-8') as fd:
        return re.sub(text_type(r':[a-z]+:`~?(.*?)`'), text_type(r'``\1``'), fd.read())


setup(
    name='emojichem',
    version='0.1',
    url='https://github.com/whitead/emoji-chem',
    license='MIT',

    author='Andrew D White',
    author_email='andrew.white@rochester.edu',

    description='Replace elements with emojis in rdkit',
    long_description=read('README.md'),

    packages=['emojichem'],

    install_requires=['rdkit-pypi'],
)
