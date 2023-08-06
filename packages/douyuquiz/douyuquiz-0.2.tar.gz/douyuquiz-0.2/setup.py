import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="douyuquiz",
    version="0.2",
    author="Minhao Zhou",
    author_email="youbao2@hotmail.com",
    description="Acquire douyu quiz information",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/youbao88/douyuquiz",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
