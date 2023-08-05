# -*- coding: utf-8 -*-
from io import open
from setuptools import setup

setup(
    name='hotxlfp',
    version='0.0.1',
    packages=['hotxlfp',],
    license='MIT',
    test_suite='tests',
    author='Leonel Câmara',
    author_email='leonelcamara@gmail.com',
    url='https://github.com/aidhound/hotxlfp',
    download_url='https://github.com/aidhound/hotxlfp/archive/0.0.1.tar.gz',
    keywords=['excel', 'formula', 'parser'],
    install_requires=open('requirements.txt', encoding="utf-8").readlines(),
    long_description='\n'.join(l for l in open('README.md', encoding="utf-8").readlines() if not l.startswith('[!')),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ]
)


