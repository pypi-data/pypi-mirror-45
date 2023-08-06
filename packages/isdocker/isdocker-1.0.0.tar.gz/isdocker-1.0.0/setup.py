import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "isdocker",
    packages = ["isdocker"],
    long_description = long_description,
    long_description_content_type = "text/markdown",
    version = "1.0.0",
    description = "Check if the process is running inside a Docker container",
    author = "Yoginth",
    author_email = "me@yoginth.com",
    url = "https://yoginth.com",
    classifiers=(
        "Programming Language :: Python",
        "Natural Language :: English",
        "Environment :: Plugins",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
    ),
    project_urls={
        'Source': 'https://gitlab.com/yoginth/isdocker',
    },
)
