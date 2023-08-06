import re
import ast
from setuptools import setup, find_packages

_version_re = re.compile(r"__version__\s+=\s+(.*)")

with open("t_rex/__init__.py", "rb") as f:
    version = str(
        ast.literal_eval(_version_re.search(f.read().decode("utf-8")).group(1))
    )

description = "Terminal Redis Explorer."

install_requirements = ["pygments", "prompt_toolkit>=2.0.0", "redis", "click"]

setup(
    name="t_rex",
    version=version,
    license="BSD",
    packages=find_packages(),
    description=description,
    long_description=open("README.md").read(),
    install_requires=install_requirements,
    entry_points="""
        [console_scripts]
        t_rex=t_rex.main:run
        t-rex=t_rex.main:run
        trex=t_rex.main:run
    """,
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: Unix",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Topic :: Database",
        "Topic :: Database :: Front-Ends",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
