import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="biodb",
    version="0.0.1",
    author="Layne Sadler",
    author_email="layne.sadler@gmail.com",
    description="Computational alchemy; Django ORM for Neo4J chemistry models.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HashRocketSyntax/biodb",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
