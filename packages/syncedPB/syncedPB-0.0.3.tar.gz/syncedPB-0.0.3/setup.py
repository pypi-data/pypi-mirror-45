import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="syncedPB",
    version="0.0.3",
    author="javirrs",
    author_email="javi.rasines@gmail.com",
    description="Synced progress bar",
    long_description="Synced progress bar for Python and iPython environments.",
    long_description_content_type="text/markdown",
    url="https://github.com/javirrs/syncedPB",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
)
 
