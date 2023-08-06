import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

l_name="pypi_lever_lib"
setuptools.setup(
    name=l_name,
    version="0.0.1",
    author="liu.changsheng",
    author_email="mail_lcs@126.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PepperPapa/xinNotes",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)