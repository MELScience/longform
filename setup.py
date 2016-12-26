import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-longform',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',
    description='A set of Django utilities to help formatting long-winded texts',
    long_description=README,
    author='MEL Science',
    author_email='dmitry.groshev@melscience.com',
    install_requires=[
        'django>=1.9',
        'bleach>=1.5.0',
        'CommonMark>=0.7.2',
        'html5lib>=0.9999999,<0.99999999',
        'pyphen>=0.9.4',
        'smartypants>=1.8.6',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.10',  # replace "X.Y" as appropriate
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # Replace these appropriately if you are stuck on Python 2.
        'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
