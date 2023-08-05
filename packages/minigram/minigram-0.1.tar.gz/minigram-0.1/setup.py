import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="minigram",
    version="0.1",
    author="DomJob",
    author_email="dominic.jobin@gmail.com",
    description="Minimalistic client API for Telegram",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DomJob/minigram",
    license="GPLv3",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)