# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='sphinxcontrib-viewsource',
    version='0.1.1',
    url='https://github.com/dgarcia360/sphinxcontrib-viewsource',
    # download_url='http://pypi.python.org/pypi/sphinxcontrib-viewsource',
    license='MIT',
    author='dgarcia360',
    author_email='dgarcia360@outlook.com',
    description='Add a "View Code" button to the literalinclude directive.',
    long_description="",
    zip_safe=True,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Topic :: Documentation',
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    platforms='any',
    include_package_data=True,
    install_requires=['Sphinx>=1.1', 'requests'],
    packages=find_packages(),
    namespace_packages=['sphinxcontrib']
)
