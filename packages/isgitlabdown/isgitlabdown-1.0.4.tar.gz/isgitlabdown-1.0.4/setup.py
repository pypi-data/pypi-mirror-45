import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "isgitlabdown",
    packages = ["isgitlabdown"],
    entry_points = {
        "console_scripts": ['isgitlabdown = isgitlabdown.isgitlabdown:main']
        },
    long_description = long_description,
    long_description_content_type = "text/markdown",
    version = "1.0.4",
    description = "Check if GitLab is down",
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
        'Source': 'https://gitlab.com/yoginth/isgitlabdown',
    },
    install_requires=[
        'requests',
    ],
)
