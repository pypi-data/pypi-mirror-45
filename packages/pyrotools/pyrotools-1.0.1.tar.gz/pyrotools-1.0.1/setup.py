import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pyrotools',
    version='1.0.1',
    packages=setuptools.find_packages(),
    url='https://github.com/NaturalBornCamper/pyrotools',
    license='Apache 2.0',
    author='NaturalBornCamper',
    author_email='pypi@naturalborncamper.com',
    description='General utils for python, used mainly for development',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
