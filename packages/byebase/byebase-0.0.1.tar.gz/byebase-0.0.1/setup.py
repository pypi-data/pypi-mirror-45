"""
@author: huongnhd
"""

from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'readme.md'), encoding='utf-8') as f:
  long_description = f.read()

with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
  install_requires = f.read(),

setup(
    name='byebase',
    version='0.0.1',

    description='package include foundation for python project',  # Optional

    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',  # Optional (see note above)

    url='https://github.com/huongnhdh/byebase.git',  # Optional

    author='huongnhd',  # Optional

    author_email='huong.nhdh@gmail.com',  # Optional

    classifiers=[
        #   3 - Alpha
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    keywords='common base development util helper adapter',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    python_requires='>=3.5, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, <4',

    install_requires=install_requires,

    extras_require={
        'dev': ['pep8', 'yapf'],
        'test': ['coverage'],
    },

    project_urls={
        'Bug Reports': 'https://github.com/pypa/sampleproject/issues',
        # 'Funding': 'https://donate.pypi.org',
        # 'Say Thanks!': 'http://saythanks.io/to/example',
        'Source': 'https://github.com/huongnhdh/byebase.git',
    },
)
