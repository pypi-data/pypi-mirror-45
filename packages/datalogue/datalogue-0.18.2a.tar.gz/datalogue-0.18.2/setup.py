import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="datalogue",
    version="0.18.2",
    author="Datalogue",
    author_email="info@datalogue.io",
    description="Datalogue SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['requests', 'python-dateutil', 'validators', 'pytest', 'numpy', 'pyyaml', 'pyarrow'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
		"Topic :: Scientific/Engineering :: Artificial Intelligence",
		"Development Status :: 3 - Alpha",
        "Operating System :: OS Independent",
    ],
)
