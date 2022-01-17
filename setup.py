import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="RadixLib",
    version="0.0.2",
    author="Omar Abdulla",
    author_email="OmarAbdulla7@hotmail.com",
    description="A Python package written to make the interaction with the Radix blockchain easier",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/0xOmarA/RadixLib",
    project_urls={
        "Bug Tracker": "https://github.com/0xOmarA/RadixLib/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Natural Language :: English",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        "wheel",
        "requests",
        "dateparser",
        "pycryptodome",
        "mnemonic",
        "hdwallet",
        "bech32",
    ],
    extras_require={
        "dev": [
            "pytest",
            "check-manifest",
            "twine"
        ]
    }
)