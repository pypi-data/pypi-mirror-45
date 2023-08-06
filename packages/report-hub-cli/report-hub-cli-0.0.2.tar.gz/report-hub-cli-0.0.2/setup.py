from setuptools import setup, find_packages
from os import path


here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='report-hub-cli',

    version='0.0.2',

    description='Cli for ReportHub server',

    long_description=long_description,

    long_description_content_type='text/markdown',

    url='https://github.com/grib9544/report-hub-cli',

    author='grib9544',

    author_email='grib9544@gmail.com',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Bug Tracking',
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],

    packages=find_packages(),

    python_requires='>=3.4',

    install_requires=['Click',
                      'requests'],

    entry_points={
        'console_scripts': [
            'report=report:cli',
        ],
    },

    project_urls={
        'Bug Reports': 'https://github.com/grib9544/report-hub-cli/issues',
        'Source': 'https://github.com/grib9544/report-hub-cli/',
    }
)