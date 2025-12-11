# setup.py
from setuptools import setup, find_packages

setup(
    name="mannered-selenium",
    version="0.1.0",
    author="tomo-k-dragon",
    author_email="tomokdragon@gmail.com",
    description="Polite web scraping using Selenium WebDriver following robots.txt",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/tomo-k-dragon/mannered-selenium",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "selenium>=4.15.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
