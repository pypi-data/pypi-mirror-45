import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()

setuptools.setup(
    name='pygore',
    version='0.0.1',
    author="Go Reverse Engineering Tool Kit",
    description="Placeholder",
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    url="https://github.com/goretk/pygore",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
)
