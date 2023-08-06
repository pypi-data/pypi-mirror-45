import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "dognamescli",
    packages = ["dognamescli"],
    entry_points = {
        "console_scripts": ['dogname = dognamescli.dognamescli:main']
        },
    long_description = long_description,
    long_description_content_type = "text/markdown",
    version = "1.0.2",
    description = "Get Awesome Random dog names in CLI!",
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
        'Patreon': 'https://www.patreon.com/yoginth',
        'Source': 'https://gitlab.com/yoginth/dognamescli',
    },
    install_requires=[
        'dognames',
    ],
)
