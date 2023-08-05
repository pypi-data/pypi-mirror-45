import pathlib
from setuptools import setup

ROOT_DIR = pathlib.Path(__file__).parent

README = (ROOT_DIR/'README.md').read_text()

setup(
    name='YTClient',
    version='1.0.0',
    url='https://github.com/JoshLee0915/youtrack-rest-python-library',
    license='https://github.com/JoshLee0915/youtrack-rest-python-library/blob/master/LICENSE',
    author='Josh Lee',
    author_email='',
    description='A rewrite of the YouTrack python API',
    long_description=README,
    long_description_content_type='text/markdown',
    packages=['YTClient'],
    install_requires=['six>=1.12.0', 'httplib2>=0.12.1'],
    python_requires='>=3.6'
)
