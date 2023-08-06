import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="easy_logging",
    version="0.0.1",
    author="Ganesh",
    author_email="ganeshraja1010@gmail.com",
    description="A quick Log Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ganeshraja10/easy_logging",
    packages=setuptools.find_packages(),
    download_url="https://github.com/ganeshraja10/easy_logging/archive/0.0.1.tar.gz",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Development Status :: 3 - Alpha',
    ],
)