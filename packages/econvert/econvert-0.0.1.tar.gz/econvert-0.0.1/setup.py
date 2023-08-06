import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="econvert",
    version="0.0.1",
    scripts=['econvert/econvert.py'],
    description="Hassle-free convertions",
    install_requires=[""],
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/YFOMNN/econvert",
    author="Mohammmed Yaseen",
    author_email="hmyaseen05@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    packages=["econvert"],
    include_package_data=True,
)
