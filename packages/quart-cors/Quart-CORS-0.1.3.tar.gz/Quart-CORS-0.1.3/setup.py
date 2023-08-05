import os
import sys

from setuptools import setup, find_packages

if sys.version_info < (3,6,1):
    sys.exit('Python 3.6.1 is the minimum required version')

PROJECT_ROOT = os.path.dirname(__file__)

with open(os.path.join(PROJECT_ROOT, 'README.rst')) as file_:
    long_description = file_.read()

INSTALL_REQUIRES = [
    'Quart>=0.6.11',
]

setup(
    name='Quart-CORS',
    version='0.1.3',
    python_requires='>=3.6.1',
    description="A Quart extension to provide Cross Origin Resource Sharing, access control, support.",
    long_description=long_description,
    url='https://gitlab.com/pgjones/quart-cors/',
    author='P G Jones',
    author_email='philip.graham.jones@googlemail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=find_packages(exclude=["tests", "tests.*"]),
    py_modules=['quart_cors'],
    install_requires=INSTALL_REQUIRES,
    tests_require=INSTALL_REQUIRES + [
        'pytest',
        'pytest-asyncio',
    ],
    include_package_data=True,
)
