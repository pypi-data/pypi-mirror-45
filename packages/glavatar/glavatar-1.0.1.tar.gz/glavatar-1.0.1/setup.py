import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "glavatar",
    packages = ["glavatar"],
    long_description = long_description,
    long_description_content_type = "text/markdown",
    version = "1.0.1",
    description = "Get the avatar of a GitLab user",
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
        'Source': 'https://gitlab.com/yoginth/glavatar',
    },
    install_requires=[
        'gitlab',
    ],
)
