from os import path
from distutils.core import setup

# The text of the README file
with open("README.md", encoding="utf-8") as f:
    LONG = f.read()

setup(
    name="hrpy",
    packages=["hrpy"],
    version="0.1.0",
    license="MIT",
    description="hr but written in python",
    long_description=LONG,
    author="John Naylor",
    author_email="jonaylor89@gmail.com",
    url="https://github.com/jonaylor89/hrpy",
    download_url="https://github.com/jonaylor89/hrpy/archive/v_1.0.tar.gz",
    keywords=["hr", "terminal", "formatting"],
    entry_points={"console_scripts": ["hr=hrpy.hr:main"]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
