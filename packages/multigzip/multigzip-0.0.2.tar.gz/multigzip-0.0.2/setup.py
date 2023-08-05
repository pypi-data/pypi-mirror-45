from setuptools import setup

from multigzip import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='multigzip',
    version=__version__,
    provides=['multigzip'],
    author='Jeff Nappi',
    url='https://github.com/ClearVoice/multigzip',
    setup_requires='setuptools',
    license='MIT',
    author_email='jeff@clearvoice.com',
    description='Multi Member GZip Support for Python 3',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['multigzip'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)
