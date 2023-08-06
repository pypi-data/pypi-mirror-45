from setuptools import setup
from codecs import open
from os import path
import warnings

version = {}
with open("version.py") as fp:
    exec(fp.read(), version)

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='entropyrate',
    author='zed.uchicago.edu',
    author_email='ishanu@uchicago.edu',
    version = str(version['__version__']),
    packages=['entropyrate'],
    scripts=[],
    url='https://github.com/zeroknowledgediscovery/',
    license='LICENSE.txt',
    description='Python wrappers for computing entropy rate of ergodic stationary finite valued processes',
    keywords=['entropy'],
    download_url='https://github.com/zeroknowledgediscovery/entropyrate/archive/'+str(version['__version__'])+'.tar.gz',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    install_requires=["numpy >= 1.6","pandas >= 0.22.0"],
    python_requires='==2.7.*',
    classifiers=[\
    'Development Status :: 4 - Beta',
    "Intended Audience :: Developers",
    "Intended Audience :: Science/Research",
    "Topic :: Scientific/Engineering :: Information Analysis",
    "Topic :: Scientific/Engineering :: Bio-Informatics",
    "Topic :: Software Development :: Libraries",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 2.7"],
    data_files=[('entropy_example/',['example/script.py','example/test.dat'])],
    include_package_data=True)
