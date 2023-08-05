import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="copypasta",
    version="0.0.1",
    author="zweicoder",
    author_email="zweicoder@gmail.com",
    description="Simple scaffolding tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zweicoder/copypasta",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
