import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "pypi_name_cli",
    packages = ["pypi_name_cli"],
    entry_points = {
        "console_scripts": ['pypi = pypi_name_cli.checkname:main']
        },
    long_description = long_description,
    long_description_content_type = "text/markdown",
    version = "0.0.2",
    description = "Check whether a package name is available on PyPI",
    author = "Yoginth",
    author_email = "me@yoginth.com",
    url = "https://yoginth.com",
    classifiers=(
        "Programming Language :: Python",
        "Natural Language :: English",
        "Environment :: Console",
        "Operating System :: OS Independent",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
    ),
    project_urls={
        'Source': 'https://gitlab.com/yoginth/pypi_name_cli',
    },
    install_requires=[
        'pypi_name',
    ],
)
