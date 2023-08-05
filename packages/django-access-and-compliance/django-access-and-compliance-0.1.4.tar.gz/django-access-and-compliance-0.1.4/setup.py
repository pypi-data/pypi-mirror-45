import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-access-and-compliance',
    version='0.1.4',
    packages=find_packages(),
    include_package_data=True,
    description='A Django application for verifying acceptance of the University of \
        Michigan\'s Data Access and Compliance Policy',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Jonathon Yu',
    install_requires=[
        'requests>=2,<3',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
