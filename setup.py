from setuptools import find_packages, setup

with open("README.md") as f:
    readme_content = f.read()

setup(
    name="notFAZuH",
    version="0.1",
    description="Discord bot for Wynncraft statistics and calculations, and other utility stuffs",
    package_dir={"": "src"},
    find_packages=find_packages(where="src"),
    long_description=readme_content,
    long_description_content_type="text/markdown",
    url="https://github.com/FAZuH/notFAZuH",
    author="FAZuH",
    author_email="fazuhhh@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.10"
)
