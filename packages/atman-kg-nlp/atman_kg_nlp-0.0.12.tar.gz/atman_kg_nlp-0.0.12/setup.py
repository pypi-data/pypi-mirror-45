import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="atman_kg_nlp",
    version="0.0.12",
    author="Jiang Shan",
    author_email="jiangshan@atman360.com",
    description="a nlp toolkit package for atman corp",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    package_data={'atman_kg_nlp': ['string_utils/trie.1.0.so']},
    install_requires=[
        'nltk >= 3.3',
        'spacy == 2.1.3'
    ],
    extras_require={
        'gpu': ['tensorflow-gpu', 'enepar[gpu]'],
        'cpu': ['tensorflow', 'benepar[cpu]']
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
