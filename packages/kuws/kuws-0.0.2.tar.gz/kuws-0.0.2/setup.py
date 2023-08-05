import setuptools

# Code originally from https://github.com/aegirhall/console-menu/blob/develop/setup.py

import io
def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)



long_description = read("README.md", "CHANGELOG.md")



setuptools.setup(
    name="kuws",
    version="0.0.2",
    author="Kieran Wood",
    author_email="kieranw098@gmail.com",
    description="A set of python scripts for common web tasks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Descent098/kuws",
    packages=["kuws"],
    install_requires=[
    "requests",
    "pytube"
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)