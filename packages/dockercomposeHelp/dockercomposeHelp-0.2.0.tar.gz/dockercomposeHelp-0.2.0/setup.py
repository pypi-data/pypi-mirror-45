import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dockercomposeHelp",
    version="0.2.0",
    author="Ariel Lima",
    author_email="ariel.lima@gordon.edu",
    description="A Python wrapper for generating a compose file",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ArielLima/dockercomposeHelp",
    packages=setuptools.find_packages(),
    install_requires=[
          'pyyaml',
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
