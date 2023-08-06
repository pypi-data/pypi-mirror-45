from os import path

from setuptools import setup, find_packages

version = "0.2.0"

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="accordion",
    packages=find_packages(),
    version=version,
    description="Make flat dict and back from dict",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Ruslan Roskoshnyj",
    author_email="i.am.yarger@gmail.com",
    url="https://github.com/newmediatech/accordion",
    download_url="https://github.com/newmediatech/accordion/archive/{}.tar.gz".format(version),
    keywords=["flat", "dict"],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    python_requires=">=2.6",
    platforms=["OS Independent"],
    license="LICENSE.txt",
    install_requires=[],
    extras_require={
        "tests": [
            "pytest (==3.4.0)",
            "coverage (==4.5)",
            "pytest-cov (==2.5.1)",
        ]
    }
)
