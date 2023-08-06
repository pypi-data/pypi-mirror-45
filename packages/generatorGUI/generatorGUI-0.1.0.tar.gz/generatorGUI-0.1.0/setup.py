from setuptools import setup, find_packages

with open("README.MD", "r") as fh:
    long_des = fh.read()

setup(
    name="generatorGUI",
    version="0.1.0",
    author="Ao Liu",
    author_email="ao@aoliu.tech",
    description="Edit parameters for the Astra generator program "
                "and run generator using a GUI.",
    license="MIT",
    keywords=["generator", "astra", "GUI", "PyQt5"],
    url="https://pypi.python.org/pypi/generatorGUI",
    packages=find_packages(),
    python_requires='>=3.0',
    long_description=long_des,
    classifiers=[
        "Development Status :: 1 - Planning",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)
