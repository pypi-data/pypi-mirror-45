import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pdfbuilder",
    version="0.1.0",
    author="Vadim Shmatov",
    author_email="shmatov96@mail.ru",
    description="A package for low-level PDF crafting",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/VadimShmatov/pdfbuilder",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5'
)
