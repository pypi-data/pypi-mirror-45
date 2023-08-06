import os
from setuptools import setup

aliases = ["pipe2codeblock", "p2c"]

here = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(here, "README.md")) as f:
    long_description = f.read()

setup(
    name="pipe2codeblock",
    version="1.0.0",
    py_modules=["pipe2codeblock"],
    license="MIT",
    author="Chris L. Barnes",
    author_email="barnesc@janelia.hhmi.org",
    entry_points={
        "console_scripts": ["{} = pipe2codeblock:main".format(a) for a in aliases]
    },
    url="https://github.com/clbarnes/pipe2codeblock",
    description="Pipe text into a code block in a markdown file.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.4",
)
