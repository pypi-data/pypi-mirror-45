import sys

#
from setuptools import setup, find_packages

# from setuptools import setup, find_packages

name = 'livyclient'
version = '0.0.2'
install_requires = [
    'requests>=2.21.0'
]

# Check Python version.

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 4)
if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write(
        f"""{name} requires Python {REQUIRED_PYTHON[0]}.{REQUIRED_PYTHON[1]}, 
        but you're trying to install it on Python {CURRENT_PYTHON[0]}.{CURRENT_PYTHON[1]}.""")
    sys.exit(1)

setup(
    name=name,
    version=version,
    description='A Python client for Apache Livy.',
    author='Deyou Lee',
    author_email='deyoulee@126.com',
    url='https://github.com/deyoulee/livyclient',
    license='GPLv3',

    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    python_requires=f'>={REQUIRED_PYTHON[0]}.{REQUIRED_PYTHON[1]}',
    zip_safe=False,
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: Chinese (Simplified)',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
    )
)
