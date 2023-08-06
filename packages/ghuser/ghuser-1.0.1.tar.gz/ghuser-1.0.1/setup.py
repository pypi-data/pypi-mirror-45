import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "ghuser",
    packages = ["ghuser"],
    long_description = long_description,
    long_description_content_type = "text/markdown",
    version = "1.0.1",
    description = "Get user info from a GitHub username",
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
        'Patreon': 'https://www.patreon.com/yoginth',
        'Source': 'https://gitlab.com/yoginth/ghuser',
    },
    install_requires=[
        'requests',
    ],
)
