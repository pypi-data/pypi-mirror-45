
import os
import setuptools

name = 'siderunner'

requires = [
    'PyVirtualDisplay',
    'selenium',
]

here = os.path.abspath(os.path.dirname(__file__))

about = {}
with open(os.path.join(here, 'siderunner', '__version__.py'), 'r', encoding='utf-8') as f:
    exec(f.read(), about)

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name=name,
    version=about['__version__'],
    author="Herb Lainchbury",
    author_email="herb@dynamic-solutions.com",
    description="Runs Selenium IDE tests without Selenium IDE.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dsilabs/" + name,
    packages=[name],
    install_requires=requires,
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
)