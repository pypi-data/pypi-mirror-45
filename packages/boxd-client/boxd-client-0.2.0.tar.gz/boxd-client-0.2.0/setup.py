#!/usr/bin/env python3

from setuptools import (
    setup,
    find_packages,
)

deps = {
    'boxd-client': [
        "eth-utils>=1.3.0,<2",
        "eth-keys>=0.2.1,<0.3.0",
        "pycryptodome>=3.6.6,<4",
        "grpcio",
        "grpcio-tools",
        "utilitybelt",
        "Crypto",
        "secp256k1",
    ],
    'test': [
        "pytest>=3.6,<3.7",
    ],
    'lint': [
        "flake8==3.5.0",
    ],
    'dev': [
        "bumpversion>=0.5.3,<1",
        "wheel",
        "setuptools>=36.2.0",
        # Fixing this dependency due to: pytest 3.6.4 has requirement pluggy<0.8,>=0.5, but you'll have pluggy 0.8.0 which is incompatible.
        "pluggy==0.7.1",
        # Fixing this dependency due to: requests 2.20.1 has requirement idna<2.8,>=2.5, but you'll have idna 2.8 which is incompatible.
        "idna==2.7",
        # idna 2.7 is not supported by requests 2.18
        "requests>=2.20,<3",
        "tox>=2.7.0",
        "twine",
    ],
}

deps['dev'] = (
    deps['boxd-client'] +
    deps['dev'] +
    deps['test'] +
    deps['lint']
)


install_requires = deps['boxd-client']

setup(
    name='boxd-client',
    # *IMPORTANT*: Don't manually change the version here. Use the 'bumpversion' utility.
    version='0.2.0',
    description=(
        "Python version sdk for boxd."
    ),
    long_description_markdown_filename='README.md',
    author='JarvisWang',
    author_email='wangjunbao2018@gmail.com',
    url='https://github.com/BOXFoundation/boxd-unpack-python',
    include_package_data=True,
    platforms=['MacOS X', 'Posix'],
    install_requires=install_requires,
    extras_require=deps,
    python_requires='>=3',
    test_requires=deps,
    setup_requires=['setuptools-markdown'],
    py_modules=['boxd_client'],
    license="MIT",
    zip_safe=False,
    keywords='boxd-client',
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
)
