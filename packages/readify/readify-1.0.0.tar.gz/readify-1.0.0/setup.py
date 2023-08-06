import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "readify",
    packages = ["readify"],
    long_description = long_description,
    long_description_content_type = "text/markdown",
    version = "1.0.0",
    description = "Convert Integer to Human Readable format",
    author = "Yoginth",
    maintainer = "Yoginth",
    author_email = "me@yoginth.com",
    maintainer_email = "me@yoginth.com",
    url = "https://yoginth.com",
    keywords = "Humanize, Readable",
    license = "MIT",
    classifiers=(
        "Programming Language :: Python",
        "Natural Language :: English",
        "Environment :: Plugins",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
    ),
    project_urls={
        'Source': 'https://gitlab.com/yoginth/readify',
    },
)
