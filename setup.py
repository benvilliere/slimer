from setuptools import setup, find_packages

setup(
    name="slimer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pyperclip",
    ],
    entry_points={
        "console_scripts": [
            "slimer=slimer.main:main",
        ],
    },
    author="Ben Villiere",
    description="A CLI tool to give a copy pasteable glance at your project structure and code.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/benvilliere/slimer",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
