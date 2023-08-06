import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pencompy",
    version="0.0.4",
    author="Michael Dubno",
    author_email="michael@dubno.com",
    description="Pencom relay controller over Ethernet",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dubnom/pencompy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
