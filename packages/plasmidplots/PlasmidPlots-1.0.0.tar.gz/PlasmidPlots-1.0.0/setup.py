import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PlasmidPlots",
    version="1.0.0",
    author="Chenkai Luo",
    author_email="chenkai.luo@gmail.com",
    description="Library for plotting gene matches on plasmids",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Chenkail/PlasmidPlots",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
