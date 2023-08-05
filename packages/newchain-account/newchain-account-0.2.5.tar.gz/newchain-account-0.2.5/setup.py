#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import (
    setup,
    find_packages,
)

extras_require={
    'test': [
        "pytest>=3.6.0",
        "tox>=2.9.1,<3",
    ],
    'lint': [
        "flake8==3.4.1",
        "isort>=4.2.15,<5",
    ],
    'doc': [
        "Sphinx>=1.6.5,<2",
        "sphinx_rtd_theme>=0.1.9",
    ],
    'dev': [
        "bumpversion>=0.5.3,<1",
        "pytest-xdist",
        "pytest-watch>=4.1.0,<5",
        "wheel",
        "ipython",
    ],
}

extras_require['dev'] = (
    extras_require['dev']
    + extras_require['test']
    + extras_require['lint']
    + extras_require['doc']
)

setup(
    name='newchain-account',
    # *IMPORTANT*: Don't manually change the version here. Use `make bump`, as described in readme
    version="0.2.5",
    description="""newchain-account: Sign NewChain transactions and messages with local private keys""",
    long_description_markdown_filename='README.md',
    author='Xia Wu',
    author_email='xiawu@zeuux.org',
    url='https://github.com/xiawu/newchain-account.py',
    include_package_data=True,
    install_requires=[
        "attrdict>=2.0.0,<3",
        "newchain-keyfile>=0.1.0",
        "newchain-keys>=0.1.0",
        "eth-utils>=1.0.2,<2",
        "hexbytes>=0.1.0,<1",
        "eth-rlp>=0.1.2,<1",
        "base58>=1.0.3",
    ],
    setup_requires=['setuptools-markdown'],
    python_requires='>=3.5, <4',
    extras_require=extras_require,
    py_modules=['newchain_account'],
    license="MIT",
    zip_safe=False,
    keywords='NewChain',
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)
