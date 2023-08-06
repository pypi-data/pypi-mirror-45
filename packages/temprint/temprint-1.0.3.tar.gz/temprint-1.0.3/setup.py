from distutils.core import setup
from temprint import __version__

VERSION = __version__
with open('README.rst') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name="temprint",
    version=VERSION,
    packages=['temprint'],
    author='Arthur Leonardo de Alencar Paulino',
    author_email='arthurleonardo.ap@gmail.com',
    url='https://github.com/arthurpaulino/temprint',
    description='An easy way to print messages intended to be overwritten.',
    long_description=LONG_DESCRIPTION,
    classifiers=['Intended Audience :: Developers',
                 'Intended Audience :: Science/Research',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: 3.7',
                 'License :: OSI Approved :: MIT License']
)
