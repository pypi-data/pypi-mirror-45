from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setup(
    name='pysicktim',
    version='0.0.8',
    description='TIM561 Python Library',
    license='GNU General Public License v3.0',
    packages=['pysicktim'],
    author='Daniyal Ansari',
    author_email='daniyal.s.ansari+pypi@gmail.com',
    keywords=['tim561'],
    url='https://github.com/ansarid/pysicktim',
    long_description=long_description,
    long_description_content_type='text/markdown'
)
