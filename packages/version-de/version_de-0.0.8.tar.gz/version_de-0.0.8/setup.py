import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='version_de',
    version='0.0.8',
    author='ishaan.kumar',
    author_email='ishaan.kumar@paytm.com',
    description="Just demo for checking how is version work",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/avneesh111995/mrchantintionpythonlibrary/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
