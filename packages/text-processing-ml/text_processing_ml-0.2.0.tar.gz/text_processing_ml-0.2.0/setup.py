import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="text_processing_ml",
    version="0.2.0",
    description="A library for processing text for machine learning",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/EricSchles/text_processing_ml",
    author="Eric Schles",
    author_email="ericschles@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    packages=['text_processing_ml',
              'text_processing_ml.normalization',
              'text_processing_ml.matching',
              'text_processing_ml.parsing'
    ],
    include_package_data=True,
    install_requires=["spacy", "nltk", "spellchecker-ml"],
)
