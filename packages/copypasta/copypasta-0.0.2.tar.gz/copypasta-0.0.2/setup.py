import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="copypasta",
    version="0.0.2",
    author="zweicoder",
    author_email="zweicoder@gmail.com",
    description="Simple scaffolding tool",
    entry_points= {
        "console_scripts": ['copypasta=copypasta.cli:cli']
    },
    install_requires=['click', 'jinja2'],
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
