import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lixi",
    version="0.0.1",
    author="LIXI",
    author_email="shane.rigby@lixi.org.au",
    description="A sample package to demonstrate LIXI2 functionality",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://lixi.org.au",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
		"Development Status :: 1 - Planning",
		"Intended Audience :: Developers",
		"License :: Other/Proprietary License"
		
    ],
)