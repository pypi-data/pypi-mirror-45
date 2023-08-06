import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="POSPair",
    version="0.0.4",
    author="Jim Macwan",
    author_email="jimmacwan94@gmail.com",
    description="Simplifying representation for natural language processing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jmacwan/POSPair",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires=[
          'pycorenlp',
          'POSPairWordEmbeddings'
      ]
)