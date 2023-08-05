"""The setup script"""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = ["tellurium", "sympy", "click", "halo", "seaborn"]

setup_requirements = ["pytest-runner"]

test_requirements = ["pytest"]

setup(
    author="Dileep Kishore",
    author_email="dkishore@bu.edu",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
    ],
    description="A kinetic model of the AHR and its regulation",
    entry_points={"console_scripts": ["iodine=pyiodine.cli:iodine"]},
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="pyiodine",
    name="pyiodine",
    packages=find_packages(include=["pyiodine"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/dileep-kishore/Iodine",
    version="0.2.0",
    zip_safe=False,
)
