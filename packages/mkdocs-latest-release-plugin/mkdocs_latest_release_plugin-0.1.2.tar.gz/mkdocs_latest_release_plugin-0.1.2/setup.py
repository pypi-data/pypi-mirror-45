from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="mkdocs_latest_release_plugin",
    version="0.1.2",
    packages=find_packages(),
    description="MkDocs plugin to display the latest version based on git tags.",
    url="https://github.com/agarthetiger/mkdocs_latest_release_plugin/",
    license="GPL v3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=3.4',
    install_requires=[
        'GitPython',
        'jinja2',
        'mkdocs>=0.17',
        'natsort',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'mkdocs.plugins': [
            'git-latest-release = mkdocs_latest_release_plugin.plugin:GitLatestReleasePlugin'
        ]
    }
)
