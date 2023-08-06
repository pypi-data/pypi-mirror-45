import io
import re
from setuptools import setup

with io.open("README.rst", "rt", encoding="utf8") as f:
    readme = f.read()

# with io.open("__version__.py", "rt", encoding="utf8") as f:
    # version = re.search(r"version = \'(.*?)\'", f.read()).group(1)
import __version__
version = __version__.version

setup(
    name="usyslog",
    version=version,
    url="https://bitbucket.org/licface/usyslog",
    project_urls={
        "Documentation": "https://bitbucket.org/licface/usyslog",
        "Code": "https://bitbucket.org/licface/usyslog",
        "Issue tracker": "https://bitbucket.org/licface/usyslog/issues",
    },
    license="BSD",
    author="Hadi Cahyadi LD",
    author_email="cumulus13@gmail.com",
    maintainer="cumulus13 Team",
    maintainer_email="cumulus13@gmail.com",
    description="Simple remote syslog sender",
    long_description=readme,
    packages=["usyslog"],
    data_files=['__version__.py', 'README.rst', 'LICENSE.rst'],
    include_package_data=True,
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
