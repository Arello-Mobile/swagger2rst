# coding: utf-8
import os
from setuptools import setup, find_packages

long_description = open('README.rst' if os.path.exists('README.rst') else 'README.md').read()

setup(
    name='swagger2rst',
    version='0.0.4',
    packages=find_packages(),
    license='MIT',
    description='Tool for convert "Swagger" format file to "Restructured text"',
    url='https://github.com/Arello-Mobile/swagger2rst',
    author='Arello Mobile',
    install_requires=open('requirements.txt').read(),
    include_package_data=True,
    test_suite='swg2rst.test',
    long_description=long_description,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Documentation',
    ],
    entry_points={
        'console_scripts': [
            'swg2rst = swg2rst.swagger2rst:main',
        ]
    }
)
