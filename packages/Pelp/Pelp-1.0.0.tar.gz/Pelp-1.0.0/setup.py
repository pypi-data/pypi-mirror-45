import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Pelp",
    version="1.0.0",
    author="Pradhit Gosula",
    author_email="pradhitg@gmail.com",
    description="A cli for Programming Language Documentation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gosulap/Pelp",
    packages=setuptools.find_packages(),
    install_requires = [], 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points = {
        "console_scripts" : [
            "pelp = pelp.cli:main"
        ]
    }
)