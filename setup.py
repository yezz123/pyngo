import os
import typing as t

import setuptools

directory = os.path.abspath(os.path.dirname(__file__))

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


def parse_requirement(req_path: str) -> t.List[str]:
    with open(os.path.join(directory, "", req_path)) as f:
        contents = f.read()
        return [i.strip() for i in contents.strip().split("\n")]


setuptools.setup(
    name="pyngo",
    version="1.0.0",
    author="Yasser Tahiri",
    platforms=["any"],
    description="Utils to help integrate pydantic into Django projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls={
        "Source Code": "https://github.com/yezz123/pyngo",
        "Bug Tracker": "https://github.com/yezz123/pyngo/issues",
        "Funding": "https://opencollective.com/yezz123",
    },
    packages=setuptools.find_packages(exclude=["tests"]),
    license="MIT",
    include_package_data=True,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Natural Language :: English",
        "Framework :: Django",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Internet :: WWW/HTTP :: Session",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
    python_requires=">=3.6",
    install_requires=parse_requirement("requirements.txt"),
)
