import setuptools

with open("../README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="latex2sympy",
    version="1.0.3",
    author="Volker Weißmann",
    author_email="volker.weissmann@gmx.de",
    description="Convert latex code to sympy code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/volkerweissmann/latex2sympy",
    packages=setuptools.find_packages(),
    install_requires=["sympy"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
    ],
)
